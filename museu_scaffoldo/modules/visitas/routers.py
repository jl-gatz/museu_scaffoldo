from fastapi import APIRouter

router_visita = APIRouter()


@router_visita.get("/")
def read_visitas():
    return {"message": "Olá, visitantes!"}
