from functools import lru_cache
from http import HTTPStatus

from fastapi import APIRouter, Depends

from museu_scaffoldo.modules.equipamentos.repository import (
    EquipamentoRepository,
)
from museu_scaffoldo.modules.equipamentos.schemas import (
    EquipamentoBase,
    EquipamentoList,
    EquipamentoPublic,
    Message,
)
from museu_scaffoldo.modules.equipamentos.service import EquipamentoService

router_equipamento = APIRouter()


# Dependência para injeção
@lru_cache
def get_repository() -> EquipamentoRepository:
    """Singleton do repositório para a aplicação."""
    return EquipamentoRepository()


async def get_service(
    repo: EquipamentoRepository = Depends(get_repository),
) -> EquipamentoService:
    return EquipamentoService(repo)


@router_equipamento.get("/", response_model=EquipamentoList)
async def read_equipamentos(
    service: EquipamentoService = Depends(get_service),
):
    equipamentos = await service.get_all_equipamentos()
    return {"equipamentos": equipamentos}


@router_equipamento.get("/{equip_id}", response_model=EquipamentoPublic)
async def read_equipamento_by_id(
    equip_id: int, service: EquipamentoService = Depends(get_service)
):
    return await service.get_equipamento_by_id(equip_id)


# GET equipamentos por nome ou marca, usando query params ou path params
@router_equipamento.get(
    "/search/{marca_ou_modelo}", response_model=EquipamentoList
)
async def read_equipamentos_by_nome(
    marca_ou_modelo: str, service: EquipamentoService = Depends(get_service)
):
    equipamentos = await service.search_equipamentos(marca_ou_modelo)
    return {"equipamentos": equipamentos}


@router_equipamento.post(
    "/", status_code=HTTPStatus.CREATED, response_model=EquipamentoPublic
)
async def create_equipamento(
    equip: EquipamentoBase, service: EquipamentoService = Depends(get_service)
):
    return await service.create_equipamento(equip)


@router_equipamento.put("/{equip_id}", response_model=EquipamentoPublic)
async def update_equipamento(
    equip_id: int,
    equip: EquipamentoBase,
    service: EquipamentoService = Depends(get_service),
):
    return await service.update_equipamento(equip_id, equip)


@router_equipamento.delete("/{equip_id}", response_model=Message)
async def delete_equipamento(
    equip_id: int, service: EquipamentoService = Depends(get_service)
):
    return await service.delete_equipamento(equip_id)
