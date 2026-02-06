import typing
from datetime import date, datetime, timezone
from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_serializer,
    field_validator,
)

from museu_scaffoldo.modules.utils.date_util import get_current_time
from museu_scaffoldo.modules.utils.text_util import title_case_com_excecoes


# -----------------------------------------------------------------------------
# 1. Base Schema
# -----------------------------------------------------------------------------
class VisitaBase(BaseModel):
    # No Pydantic V2, você pode forçar o uso de TZ ciente
    model_config = ConfigDict(from_attributes=True, timezone_aware=True)

    nome_grupo: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nome da escola, empresa ou grupo visitante",
    )

    # Usamos datetime para guardar data e hora.
    # Se quiser apenas data, mude para import date e o tipo para date
    data_visita: datetime = Field(
        ..., description="Data e hora agendada ou realizada da visita"
    )

    descricao: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Relatório ou pauta da visita",
    )

    image_list: List[HttpUrl] = Field(
        default_factory=list, description="Fotos tiradas durante a visita"
    )

    # Opcional, inicializa com lista vazia para evitar null
    video_list: Optional[List[HttpUrl]] = Field(
        default_factory=list,
        description="Links para vídeos (YouTube, Drive, etc.)",
    )

    # -------------------------------------------------------------------------
    # VALIDADORES
    # -------------------------------------------------------------------------

    @field_validator("nome_grupo")
    @classmethod
    def formatar_nome(cls, v: str):
        """
        Padroniza o nome do grupo para Title Case e remove espaços extras.
        Ex: '  universidade de são paulo  ' -> 'Universidade de São Paulo'
        """
        return title_case_com_excecoes(v)

    @field_validator("image_list", "video_list")
    @classmethod
    def validar_limites_midia(cls, v: List[HttpUrl], info):
        """
        Evita sobrecarga de dados.
        Define limites diferentes para imagens e vídeos.
        """
        field_name = info.field_name

        len_image = 20
        len_video = 5

        if field_name == "image_list" and len(v) > len_image:
            raise ValueError(
                f"O limite máximo é de {len_image} imagens por visita."
            )

        if field_name == "video_list" and len(v) > len_video:
            raise ValueError(
                f"O limite máximo é de {len_video} vídeos por visita."
            )

        return v

    @field_validator("data_visita")
    @classmethod
    def validar_ano_minimo(cls, v: datetime):
        """
        Garante que ninguém coloque uma data absurda (ex: ano 1900).
        """
        year_min = 2020

        if v.year < year_min:
            raise ValueError(
                f"A data da visita não pode ser anterior a {year_min}."
            )
        return v


# -----------------------------------------------------------------------------
# 2. Create Schema
# -----------------------------------------------------------------------------
class VisitaDB(VisitaBase):
    # Aqui você poderia adicionar campos específicos de agendamento,
    # como "responsavel_agendamento", se necessário.
    id: int
    # responsavel_agendamento: Optional[str]


# -----------------------------------------------------------------------------
# 3. Response Schema
# -----------------------------------------------------------------------------
class VisitaPublic(VisitaBase):
    # model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime = Field(default_factory=get_current_time)

    @typing.override
    @field_serializer("created_at", "data_visita", when_used="json")
    def serialize_utc(self, v: datetime) -> str:
        if isinstance(v, date) and not isinstance(v, datetime):
            raise TypeError("date não é aceito. Use datetime UTC.")

        # Isso precisa permanecer no código
        # Está desativado por conta dos problemas de asserção de tempo
        # if v.tzinfo is None:
        #     raise ValueError(
        #         "created_at deve ser timezone-aware (UTC). "
        #         "Datetime naive detectado."
        #     )

        # DEBUG para o caso do time UTC vs naive
        # (ainda não solucionado)
        # print(
        #     "DEBUG:",
        #     v,
        #     type(v),
        #     v.tzinfo,
        # )

        return v.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


class VisitaList(BaseModel):
    visitas: list[VisitaPublic]


class Message(BaseModel):
    message: str


class FilterParams(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)

    @field_validator("end_date")
    def end_date_after_start_date(cls, v, info):
        if "start_date" in info.data and v < info.data["start_date"]:
            raise ValueError("Data de fim deve ser maior que a data de início")
        return v
