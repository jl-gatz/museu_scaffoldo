from datetime import date
from typing import Optional

from pydantic import BaseModel


class EquipamentoSchema(BaseModel):
    id: int
    marca: str
    modelo: str
    descricao: str
    numero_serie: str
    data_aquisicao: date
    data_ultima_manutencao: Optional[date] = None
    status_operacional: bool

    class Config:
        orm_mode = True
        from_attributes = True
