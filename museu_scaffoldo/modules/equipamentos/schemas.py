from typing import List, Optional

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
)

from .marcas.marcas_e_modelos import MarcasNomesNormalizados


# -----------------------------------------------------------------------------
# 1. Base Schema: Campos comuns usados tanto na criação quanto na leitura
# -----------------------------------------------------------------------------
class EquipamentoBase(BaseModel):
    marca: str = Field(
        ..., min_length=2, max_length=50, description="Marca do fabricante"
    )
    modelo: str = Field(
        ..., min_length=2, max_length=50, description="Modelo do equipamento"
    )
    descricao: Optional[str] = Field(
        None, max_length=500, description="Detalhes técnicos ou observações"
    )

    # HttpUrl garante que a string seja uma URL válida (http/https)
    url: Optional[HttpUrl] = Field(
        None, description="Link para o site do fabricante ou manual"
    )

    imagem: Optional[HttpUrl] = Field(
        None, description="URL da imagem principal (thumbnail)"
    )

    lista_imagens: List[HttpUrl] = Field(
        default_factory=list, description="Lista de URLs com fotos adicionais"
    )

    qr_code: Optional[str] = Field(
        None, description="Código ou Hash para geração do QR Code"
    )

    # -------------------------------------------------------------------------
    # VALIDADORES (A mágica acontece aqui)
    # -------------------------------------------------------------------------

    @field_validator("marca", "modelo")
    @classmethod
    def formatar_texto(cls, v: str):
        """
        Validador 1: Normalização de Texto
        Remove espaços em branco nas pontas e coloca em Title Case.
        Ex: '  sony  ' vira 'Sony'
        """
        marcas_str = {m.value.upper(): m for m in MarcasNomesNormalizados}

        if v.upper() in marcas_str:
            return v.upper()

        return v.strip().title()

    @field_validator("qr_code")
    @classmethod
    def validar_qr_code(cls, v: str):
        """
        Validador 2: Regra de Negócio para QR Code
        Exemplo: Obriga o código a ser alfanumérico e maiúsculo.
        """
        if v and not v.isalnum():
            raise ValueError("O QR Code deve conter apenas letras e números.")
        return v.upper() if v else v

    @field_validator("lista_imagens")
    @classmethod
    def limitar_imagens(cls, v: List[HttpUrl]):
        """
        Validador 3: Limite de Lista
        Impede que o usuário envie 500 fotos de uma vez.
        """
        limite = 10
        if len(v) > limite:
            raise ValueError("O limite máximo é de 10 imagens adicionais.")
        return v

    @model_validator(mode="after")
    def checar_imagem_principal(self):
        """
        Validador 4: Validação Cruzada (Cross-Field)
        Se não houver imagem principal, mas houver uma lista,
        pega a primeira da lista e define como principal.
        """
        if not self.imagem and self.lista_imagens:
            self.imagem = self.lista_imagens[0]
        return self


# -----------------------------------------------------------------------------
# 2. Create Schema: O que o usuário envia para criar (POST)
# -----------------------------------------------------------------------------
class EquipamentoDB(EquipamentoBase):
    # Aqui poderíamos adicionar campos obrigatórios apenas na criação,
    # mas neste caso, a base já cobre tudo.
    id: int


# -----------------------------------------------------------------------------
# 3. Response Schema: O que a API devolve (GET)
# -----------------------------------------------------------------------------
class EquipamentoPublic(EquipamentoBase):
    id: int

    class Config:
        # Permite que o Pydantic leia dados de objetos ORM (como SQLAlchemy)
        from_attributes = True


class EquipamentoList(BaseModel):
    equipamentos: list[EquipamentoPublic]


class Message(BaseModel):
    message: str
