# service.py
from typing import List

from fastapi import HTTPException, status

from .interfaces import IEquipamentoRepository
from .schemas import EquipamentoBase, EquipamentoPublic


class EquipamentoService:
    def __init__(self, repository: IEquipamentoRepository):
        self.repository = repository

    async def create_equipamento(
        self, equip_data: EquipamentoBase
    ) -> EquipamentoPublic:
        """Cria um novo equipamento com validações de negócio"""
        # Aqui podem entrar validações adicionais
        equipamento = await self.repository.create(equip_data)
        return EquipamentoPublic(**equipamento.model_dump())

    async def get_equipamento_by_id(self, equip_id: int) -> EquipamentoPublic:
        equipamento = await self.repository.get_by_id(equip_id)
        if not equipamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipamento não encontrado",
            )
        return EquipamentoPublic(**equipamento.model_dump())

    async def get_all_equipamentos(self) -> List[EquipamentoPublic]:
        equipamentos = await self.repository.get_all()
        return [EquipamentoPublic(**e.model_dump()) for e in equipamentos]

    async def search_equipamentos(self, termo: str) -> List[EquipamentoPublic]:
        equipamentos = await self.repository.get_by_marca_or_modelo(termo)
        if not equipamentos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum equipamento encontrado com o termo buscado",
            )
        return [EquipamentoPublic(**e.model_dump()) for e in equipamentos]

    async def update_equipamento(
        self, equip_id: int, equip_data: EquipamentoBase
    ) -> EquipamentoPublic:
        equipamento = await self.repository.update(equip_id, equip_data)
        if not equipamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipamento não encontrado",
            )
        return EquipamentoPublic(**equipamento.model_dump())

    async def delete_equipamento(self, equip_id: int) -> dict:
        deleted = await self.repository.delete(equip_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipamento não encontrado",
            )
        return {"message": "Equipamento removido com sucesso"}
