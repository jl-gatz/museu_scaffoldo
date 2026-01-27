from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class VisitaSchema(BaseModel):
    id: int
    visitante_nome: str
    data_visita: date
    hora_entrada: time
    hora_saida: Optional[time] = None
    guia_turistico: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
