from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from museu_scaffoldo import main


@pytest.fixture
def client():
    return TestClient(main.app)


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'status': 'ok',
        'API users': 'O serviço de usuários está ok',
        'API equipamentos': 'O serviço de equipamentos está ok',
        'API visitas': 'O serviço de visitas está ok',
        'message': 'API rodando com sucesso!',
    }
