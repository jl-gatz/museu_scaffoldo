from fastapi import APIRouter, FastAPI

from museu_scaffoldo.modules.equipamentos.routers import router_equipamento
from museu_scaffoldo.modules.users.routers import router_user
from museu_scaffoldo.modules.visitas.routers import router_visita

app = FastAPI(title='API do Museu de Informática')
router = APIRouter()

router.include_router(router_user, prefix='/users', tags=['Users'])
router.include_router(
    router_equipamento, prefix='/equipamentos', tags=['Equipamentos']
)
router.include_router(router_visita, prefix='/visitas', tags=['Visitas'])
