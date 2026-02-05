from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from museu_scaffoldo.modules.visitas.schemas import (
    FilterParams,
    Message,
    VisitaBase,
    VisitaDB,
    VisitaList,
    VisitaPublic,
)

from .service import fake_visitas_db, get_visitas

router_visita = APIRouter()

# Teste com database falso
database = fake_visitas_db


@router_visita.get(
    "/{visita_id}", status_code=HTTPStatus.OK, response_model=VisitaPublic
)
def read_visita_by_id(visita_id: int):
    if visita_id > len(database) or visita_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Visita não encontrada"
        )
    visita_with_id = database[visita_id - 1]

    return visita_with_id


@router_visita.get("/", response_model=VisitaList)
def read_visitas(params: Annotated[FilterParams, Query()]):
    """
    Retorna a lista de visitas.
    - Permite paginação (skip/limit).
    - Permite filtrar por intervalo de datas (inicio/fim).
    """
    return {
        "visitas": get_visitas(
            skip=params.skip,
            limit=params.limit,
            start_date=params.start_date,
            end_date=params.end_date,
        )
    }


@router_visita.post(
    "/", status_code=HTTPStatus.CREATED, response_model=VisitaPublic
)
def create_visita(visita: VisitaBase):
    visita_with_id = VisitaDB(**visita.model_dump(), id=len(database) + 1)
    database.append(visita_with_id)
    return visita_with_id


@router_visita.put("/{visita_id}", response_model=VisitaPublic)
def update_visita(visita_id: int, visita: VisitaBase):
    if visita_id > len(database) or visita_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Visita não encontrada"
        )
    visita_with_id = VisitaDB(**visita.model_dump(), id=visita_id)
    database[visita_id - 1] = visita_with_id
    return visita_with_id


@router_visita.delete("/{visita_id}", response_model=Message)
def delete_visita(visita_id: int):
    if visita_id > len(database) or visita_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Visita não encontrada"
        )
    del database[visita_id - 1]
    return {"message": "Visita deletada com sucesso!"}
