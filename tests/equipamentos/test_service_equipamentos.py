# tests/test_service.py
from http import HTTPStatus

import pytest
from fastapi import HTTPException

from museu_scaffoldo.modules.equipamentos.schemas import EquipamentoBase


@pytest.mark.asyncio
async def test_service_create_equipamento(service, sample_equipamento_data):
    result = await service.create_equipamento(
        EquipamentoBase(**sample_equipamento_data)
    )

    assert result.id == 1
    assert result.marca == "IBM"


@pytest.mark.asyncio
async def test_service_get_equipamento_by_id_not_found(service):
    with pytest.raises(HTTPException) as exc:
        await service.get_equipamento_by_id(999)
    assert exc.value.status_code == HTTPStatus.NOT_FOUND
