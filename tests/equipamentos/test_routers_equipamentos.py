from http import HTTPStatus

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from museu_scaffoldo.modules.equipamentos import routers
from museu_scaffoldo.modules.equipamentos.routers import (
    read_equipamento_by_id,
    read_equipamento_by_nome,
)

app = FastAPI()
app.include_router(routers.router_equipamento)


@pytest.fixture
def client():
    return TestClient(app)


def test_create_equipamento(client: TestClient):
    jasao = {
        "marca": "IBM",
        "modelo": "HAL 9000",
        "descricao": "Heuristically programmed Algorithmic computer.",
        "imagem": "http://example.com/imagem1.jpg",
        "lista_imagens": [
            "http://example.com/ibagem1.jpg",
            "http://example.com/ibagem2.jpg",
        ],
        "url": "https://en.wikipedia.org/wiki/HAL_9000",
        "qr_code": "ab1234",
    }

    response = client.post("/", json=jasao)  # noqa: F811
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
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


def test_read_equipamentos(client: TestClient):
    response = client.get("/")  # noqa: F811
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "equipamentos": [
            {
                "id": 1,
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
        ]
    }


@pytest.mark.parametrize(
    ("equip_id", "expected_marca", "should_error"),
    [(1, "IBM", False), (2, "Cobra", True), (999, None, True)],
)
def test_read_equip_by_id(
    equip_id: int, expected_marca: str, should_error: bool
):
    if should_error:
        with pytest.raises(HTTPException) as excinfo:
            read_equipamento_by_id(equip_id)

        assert excinfo.value.status_code == HTTPStatus.NOT_FOUND
    else:
        response = read_equipamento_by_id(equip_id)
        assert response.marca == expected_marca
        assert response.id == equip_id


@pytest.mark.parametrize(
    ("search_marca_model", "should_error"),
    [("IBM", False), ("Cobra", True), ("XPTO", True)],
)
def test_read_equip_by_marca_modelo(
    search_marca_model: str, should_error: bool
):
    print(f"Busca por: '{search_marca_model}' (Deve dar erro? {should_error})")

    if should_error:
        with pytest.raises(HTTPException) as excinfo:
            read_equipamento_by_nome(search_marca_model)

        assert excinfo.value.status_code == HTTPStatus.NOT_FOUND
        assert excinfo.value.detail == "Marca ou modelo não encontrado"
    else:
        response = read_equipamento_by_nome(search_marca_model)
        lista_equipamentos = response["equipamentos"]
        print(f"Equipamentos encontrados: {lista_equipamentos}")

        # Verifica se a lista não está vazia
        for equip in lista_equipamentos:
            assert len(lista_equipamentos) > 0
            assert (
                search_marca_model.lower() in equip.marca.lower()
                or search_marca_model.lower() in equip.modelo.lower()
            )


def test_update_equipamento(client: TestClient):
    jasao = {
        "id": 1,
        "marca": "IBM",
        "modelo": "HAL 9000",
        "descricao": "Heuristically programmed Algorithmic computer.",
        "imagem": "http://example.com/imagem33.jpg",
        "lista_imagens": [
            "http://example.com/ibagem48.jpg",
            "http://example.com/ibagem64.jpg",
        ],
        "url": "https://en.wikipedia.org/wiki/HAL_9000",
        "qr_code": "AB1234",
    }
    response = client.put("/1", json=jasao)  # noqa: F811
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "marca": "IBM",
        "modelo": "HAL 9000",
        "descricao": "Heuristically programmed Algorithmic computer.",
        "imagem": "http://example.com/imagem33.jpg",
        "lista_imagens": [
            "http://example.com/ibagem48.jpg",
            "http://example.com/ibagem64.jpg",
        ],
        "url": "https://en.wikipedia.org/wiki/HAL_9000",
        "qr_code": "AB1234",
    }


def test_delete_equipamento(client: TestClient):
    response = client.delete("/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Equipamento deletado com sucesso!"}


def test_read_equipamento_nao_encontrado(client: TestClient):
    response = client.get("/-1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Equipamento não encontrado"}


def test_update_equipamento_nao_encontrado(client: TestClient):
    jasao = {
        "id": 1,
        "marca": "IBM",
        "modelo": "HAL 9000",
        "descricao": "Heuristically programmed Algorithmic computer.",
        "imagem": "http://example.com/imagem33.jpg",
        "lista_imagens": [
            "http://example.com/ibagem48.jpg",
            "http://example.com/ibagem64.jpg",
        ],
        "url": "https://en.wikipedia.org/wiki/HAL_9000",
        "qr_code": "AB1234",
    }

    response = client.put("/-1", json=jasao)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Equipamento não encontrado"}


def test_delete_equipamento_nao_encontrado(client: TestClient):
    response = client.delete("/-1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Equipamento não encontrado"}
