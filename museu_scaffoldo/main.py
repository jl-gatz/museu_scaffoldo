# main.py
from fastapi import FastAPI

from museu_scaffoldo.core.api.v1.routers import router
from museu_scaffoldo.core.api.v1.schemas import HealthCheckSchema

app = FastAPI(title="API do Museu de Informática")

# Incluindo as rotas dos apps com prefixos
app.include_router(router, prefix="/api/v1")


@app.get("/", response_model=HealthCheckSchema)
def health_check():
    # Apenas para o health_check
    user_service = None
    visitas_service = None
    equips_service = None

    users_api = router.get("/users/")
    visitas_api = router.get("/visitas/")
    equips_api = router.get("/equipamentos/")

    if users_api:
        user_service = "ok"

    if visitas_api:
        visitas_service = "ok"

    if equips_api:
        equips_service = "ok"

    return {
        "status": "ok",
        "API_users": f"O serviço de usuários está {user_service}",
        "API_equipamentos": f"O serviço de equipamentos está {equips_service}",
        "API_visitas": f"O serviço de visitas está {visitas_service}",
        "message": "API rodando com sucesso!",
    }
