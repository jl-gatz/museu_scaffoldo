# repository.py
from typing import List, Optional

from .interfaces import IEquipamentoRepository
from .schemas import EquipamentoBase, EquipamentoDB


class EquipamentoRepository(IEquipamentoRepository):
    def __init__(self):
        self._database: List[EquipamentoDB] = []

    async def create(self, equipamento: EquipamentoBase) -> EquipamentoDB:
        novo_id = len(self._database) + 1
        equip_with_id = EquipamentoDB(**equipamento.model_dump(), id=novo_id)
        self._database.append(equip_with_id)
        return equip_with_id

    async def get_by_id(self, equip_id: int) -> Optional[EquipamentoDB]:
        if 1 <= equip_id <= len(self._database):
            return self._database[equip_id - 1]
        return None

    async def get_all(self) -> List[EquipamentoDB]:
        return self._database.copy()

    async def get_by_marca_or_modelo(self, termo: str) -> List[EquipamentoDB]:
        termo_lower = termo.lower()
        return [
            equip
            for equip in self._database
            if termo_lower in equip.marca.lower()
            or termo_lower in equip.modelo.lower()
        ]

    async def update(
        self, equip_id: int, equipamento: EquipamentoBase
    ) -> Optional[EquipamentoDB]:
        if 1 <= equip_id <= len(self._database):
            equip_with_id = EquipamentoDB(
                **equipamento.model_dump(), id=equip_id
            )
            self._database[equip_id - 1] = equip_with_id
            return equip_with_id
        return None

    async def delete(self, equip_id: int) -> bool:
        if 1 <= equip_id <= len(self._database):
            self._database.pop(equip_id - 1)
            # Reindexar os IDs? (opcional)
            for i, equip in enumerate(self._database, start=1):
                equip.id = i
            return True
        return False
