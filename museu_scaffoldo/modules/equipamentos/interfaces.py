# interfaces.py
from abc import ABC, abstractmethod
from typing import List, Optional

from .schemas import EquipamentoBase, EquipamentoDB


class IEquipamentoRepository(ABC):
    @abstractmethod
    async def create(self, equipamento: EquipamentoBase) -> EquipamentoDB:
        """Cria um novo equipamento"""
        pass

    @abstractmethod
    async def get_by_id(self, equip_id: int) -> Optional[EquipamentoDB]:
        """Busca equipamento por ID"""
        pass

    @abstractmethod
    async def get_all(self) -> List[EquipamentoDB]:
        """Lista todos os equipamentos"""
        pass

    @abstractmethod
    async def get_by_marca_or_modelo(self, termo: str) -> List[EquipamentoDB]:
        """Busca por marca ou modelo"""
        pass

    @abstractmethod
    async def update(
        self, equip_id: int, equipamento: EquipamentoBase
    ) -> Optional[EquipamentoDB]:
        """Atualiza um equipamento"""
        pass

    @abstractmethod
    async def delete(self, equip_id: int) -> bool:
        """Remove um equipamento"""
        pass
