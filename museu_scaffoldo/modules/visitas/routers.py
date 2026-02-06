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
def read_visita_by_id(visita_id: int) -> VisitaPublic:
    """
    Retorna um objeto visita pelo id

    Args:
        visita_id (int): O id do objeto que queremos retornar

    Raises:
        HTTPException: Erro 404 (not found) para o caso de id não encontrado

    Returns:
        VisitaPublic: Retorna a visita com id pesquisado
    """
    if visita_id > len(database) or visita_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Visita não encontrada"
        )
    visita_with_id = database[visita_id - 1]

    return visita_with_id


@router_visita.get("/", response_model=VisitaList)
def read_visitas(params: Annotated[FilterParams, Query()]) -> VisitaList:
    """
    Lista todas as visitas e inclui a possibilidade de listar com
    skip, limit e por período.

    Args:
        params (Annotated[FilterParams, Query):
        params retorna todos os parâmetros possíveis para a função:
        skip:  Ignorar n resultados
        limit: Paginação
        start_date: Para pesquisa por período, data de início
        end_date: Para pesquisa por perído, data de fim

    Returns:
        VisitaList: Retorna uma lista de visitas
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
def create_visita(visita: VisitaBase) -> VisitaPublic:
    """
    Cria uma visita no sistema.

    Args:
        visita (VisitaBase): O schema base para criação do objeto visita

    Returns:
        VisitaPublic: Retorna a visita com id pesquisado
    """
    visita_with_id = VisitaDB(**visita.model_dump(), id=len(database) + 1)
    database.append(visita_with_id)
    return visita_with_id


@router_visita.put("/{visita_id}", response_model=VisitaPublic)
def update_visita(visita_id: int, visita: VisitaBase) -> VisitaPublic:
    """
    Atualiza o objeto de id 'visita_id'

    Args:
        visita_id (int): O id da visita que queremos editar
        visita (VisitaBase): O schema base para criação/edição do objeto visita

    Raises:
        HTTPException: Erro 404 (not found) para o caso de id não encontrado

    Returns:
        VisitaPublic: Retorna a visita atualizada com id pesquisado
    """
    if visita_id > len(database) or visita_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Visita não encontrada"
        )
    visita_with_id = VisitaDB(**visita.model_dump(), id=visita_id)
    database[visita_id - 1] = visita_with_id
    return visita_with_id


@router_visita.delete("/{visita_id}", response_model=Message)
def delete_visita(visita_id: int) -> Message:
    """
    Apaga o objeto visita de id 'visita_id'
    Args:
        visita_id (int): O id da visita que queremos deletar

    Raises:
        HTTPException: Erro 404 (not found) para o caso de id não encontrado

    Returns:
        Message: Mensagem de 'visita deletada com sucesso'
    """
    if visita_id > len(database) or visita_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Visita não encontrada"
        )
    del database[visita_id - 1]
    return {"message": "Visita deletada com sucesso!"}
