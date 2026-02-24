import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from museu_scaffoldo.modules.equipamentos.repository import (
    EquipamentoRepository,
)
from museu_scaffoldo.modules.equipamentos.routers import (
    get_repository,
    router_equipamento,
)
from museu_scaffoldo.modules.equipamentos.service import EquipamentoService


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router_equipamento)
    return app


@pytest.fixture
def repo():
    """Um repositório novo para cada teste."""
    return EquipamentoRepository()


@pytest.fixture
def service(repo):
    return EquipamentoService(repo)


@pytest.fixture
def client(app, repo):
    """
    Cliente de teste com a dependência get_repository
    sobrescrita para usar o repo do fixture.
    """
    app.dependency_overrides[get_repository] = lambda: repo
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()  # limpa após o teste


@pytest.fixture
def sample_equipamento_data():
    return {
        "marca": "IBM",
        "modelo": "HAL 9000",
        "descricao": "Heuristically programmed Algorithmic computer.",
        "imagem": "http://example.com/imagem1.jpg",
        "lista_imagens": [
            "http://example.com/ibagem1.jpg",
            "http://example.com/ibagem2.jpg",
        ],
        "url": "https://en.wikipedia.org/wiki/HAL_9000",
        "qr_code": "AB1234",
    }
