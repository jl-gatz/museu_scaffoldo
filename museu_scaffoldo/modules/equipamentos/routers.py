from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from museu_scaffoldo.modules.equipamentos.schemas import (
    EquipamentoBase,
    EquipamentoDB,
    EquipamentoList,
    EquipamentoPublic,
    Message,
)

router_equipamento = APIRouter()

# Teste com database falso
database = []


@router_equipamento.get("/", response_model=EquipamentoList)
def read_equipamentos():
    return {"equipamentos": database}


@router_equipamento.get(
    "/{equip_id}", status_code=HTTPStatus.OK, response_model=EquipamentoPublic
)
def read_equipamento_by_id(equip_id: int):
    if equip_id > len(database) or equip_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Equipamento não encontrado",
        )
    user_with_id = database[equip_id - 1]

    return user_with_id


# GET equipamentos por nome ou marca, usando query params ou path params
@router_equipamento.get(
    "/search/{marca_ou_modelo}",
    status_code=HTTPStatus.OK,
    response_model=EquipamentoList,
)
def read_equipamento_by_nome(marca_ou_modelo: str):
    equipamentos_encontrados = [
        equip
        for equip in database
        if marca_ou_modelo.lower() in equip.marca.lower()
        or marca_ou_modelo.lower() in equip.modelo.lower()
    ]
    if not equipamentos_encontrados:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Marca ou modelo não encontrado",
        )
    return {"equipamentos": equipamentos_encontrados}


@router_equipamento.post(
    "/", status_code=HTTPStatus.CREATED, response_model=EquipamentoPublic
)
def create_equipamento(equip: EquipamentoBase):
    equip_with_id = EquipamentoDB(**equip.model_dump(), id=len(database) + 1)
    database.append(equip_with_id)
    return equip_with_id


@router_equipamento.put("/{equip_id}", response_model=EquipamentoPublic)
def update_user(equip_id: int, equip: EquipamentoBase):
    if equip_id > len(database) or equip_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Equipamento não encontrado",
        )
    user_with_id = EquipamentoDB(**equip.model_dump(), id=equip_id)
    database[equip_id - 1] = user_with_id
    return user_with_id


@router_equipamento.delete("/{equip_id}", response_model=Message)
def delete_user(equip_id: int):
    if equip_id > len(database) or equip_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Equipamento não encontrado",
        )
    del database[equip_id - 1]
    return {"message": "Equipamento deletado com sucesso!"}
