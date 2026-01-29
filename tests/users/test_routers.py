from http import HTTPStatus

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from museu_scaffoldo.modules.users import routers
from museu_scaffoldo.modules.users.deps import get_current_user

app = FastAPI()
app.include_router(routers.router_user)


@pytest.fixture
def client():
    return TestClient(app)


def override_get_current_user():
    return {
        'id': 1,
        'username': 'Beltrano',
        'email': 'mock@beltrano.com',
        'password': '123456',
    }


app.dependency_overrides[get_current_user] = override_get_current_user


def test_create_user(client):
    jasao = {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }

    response = client.post('/', json=jasao)  # noqa: F811
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/')  # noqa: F811
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'alice',
                'email': 'alice@example.com',
            }
        ]
    }


def test_read_users_me(client):
    response = client.get('/me')  # noqa: F811
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Beltrano',
        'email': 'mock@beltrano.com',
    }


def test_update_user(client):
    jasao = {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'mynewpassword',
    }
    response = client.put('/1', json=jasao)  # noqa: F811
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@example.com',
    }


def test_delete_user(client):
    response = client.delete('/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário deletado com sucesso!'}
