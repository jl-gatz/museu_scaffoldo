# tests/test_repository.py
import pytest

from museu_scaffoldo.modules.equipamentos.schemas import EquipamentoBase


@pytest.mark.asyncio
async def test_create_equipamento(repo, sample_equipamento_data):
    equip_data = EquipamentoBase(**sample_equipamento_data)
    result = await repo.create(equip_data)

    assert result.id == 1
    assert result.marca == "IBM"
    assert result.modelo == "HAL 9000"


@pytest.mark.asyncio
async def test_get_by_id(repo, sample_equipamento_data):
    equip_data = EquipamentoBase(**sample_equipamento_data)
    await repo.create(equip_data)

    result = await repo.get_by_id(1)
    assert result is not None
    assert result.id == 1

    not_found = await repo.get_by_id(999)
    assert not_found is None
