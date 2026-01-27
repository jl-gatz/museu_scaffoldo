# main.py
from fastapi import FastAPI

from museu_scaffoldo.modules.equipamentos.routers import (
    router_equipamento as equipamentos_router,
)
from museu_scaffoldo.modules.users.routers import router_user as users_router
from museu_scaffoldo.modules.visitas.routers import (
    router_visita as visitas_router,
)

app = FastAPI(title='API do Museu de Informática')

# Incluindo as rotas dos apps com prefixos
app.include_router(users_router)
app.include_router(
    equipamentos_router, prefix='/equipamentos', tags=['Equipamentos']
)
app.include_router(visitas_router, prefix='/visitas', tags=['Visitas'])


@app.get('/')
def health_check():
    # Apenas para o health_check
    user_service = None
    visitas_service = None
    equips_service = None

    users_api = users_router.get('/')
    visitas_api = visitas_router.get('/')
    equips_api = equipamentos_router.get('/')

    if users_api:
        user_service = 'ok'

    if visitas_api:
        visitas_service = 'ok'

    if equips_api:
        equips_service = 'ok'

    print(users_api)
    return {
        'status': 'ok',
        'API users': f'O serviço de usuários está {user_service}',
        'API equipamentos': f'O serviço de equipamentos está {equips_service}',
        'API visitas': f'O serviço de visitas está {visitas_service}',
        'message': 'API rodando com sucesso!',
    }
