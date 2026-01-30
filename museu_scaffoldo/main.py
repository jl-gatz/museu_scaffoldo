# main.py
from fastapi import FastAPI

from museu_scaffoldo.core.api.v1.routers import router

app = FastAPI(title='API do Museu de Informática')

# Incluindo as rotas dos apps com prefixos
app.include_router(router, prefix='/api/v1')


@app.get('/')
def health_check():
    # Apenas para o health_check
    user_service = None
    visitas_service = None
    equips_service = None

    users_api = router.get('/users/')
    visitas_api = router.get('/visitas/')
    equips_api = router.get('/equipamentos/')

    if users_api:
        user_service = 'ok'

    if visitas_api:
        visitas_service = 'ok'

    if equips_api:
        equips_service = 'ok'

    return {
        'status': 'ok',
        'API users': f'O serviço de usuários está {user_service}',
        'API equipamentos': f'O serviço de equipamentos está {equips_service}',
        'API visitas': f'O serviço de visitas está {visitas_service}',
        'message': 'API rodando com sucesso!',
    }
