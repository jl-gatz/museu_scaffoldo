from fastapi import APIRouter

router_equipamento = APIRouter()


@router_equipamento.get('/')
def read_equipamentos():
    return {'message': 'Olá, equipamentos!'}
