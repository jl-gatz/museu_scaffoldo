from http import HTTPStatus

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from museu_scaffoldo.modules.visitas import routers
from museu_scaffoldo.modules.visitas.routers import read_visita_by_id

app = FastAPI()
app.include_router(routers.router_visita)


@pytest.fixture
def client():
    return TestClient(app)


def test_create_visita_compara_data(client: TestClient, frozen_time):
    jasao = {
        "nome_grupo": "Grupo Escolar José Mojica Marins",
        "data_visita": "2024-10-15T14:30:00Z",
        "descricao": "Trampo técnico, mezzo aliche mezzo catupiry",
        "image_list": [
            "https://minha-bucket.s3.aws.com/foto1.jpg",
            "https://minha-bucket.s3.aws.com/foto2.jpg",
        ],
        "video_list": ["https://youtube.com/watch?v=exemplo"],
    }

    response = client.post("/", json=jasao)  # noqa: F811
    payload = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert "created_at" in payload
    assert payload["created_at"].endswith("Z")


def test_create_visita_sem_data(client: TestClient):
    jasao = {
        "nome_grupo": "Escola Estadual e Cordão de Samba Rock B Negão",
        "data_visita": "2024-10-15T14:30:00Z",
        "descricao": "Trampo técnico, mezzo aliche mezzo catupiry",
        "image_list": [
            "https://minha-bucket.s3.aws.com/foto1.jpg",
            "https://minha-bucket.s3.aws.com/foto2.jpg",
        ],
        "video_list": ["https://youtube.com/watch?v=exemplo"],
    }

    response = client.post("/", json=jasao)  # noqa: F811
    payload = response.json()

    if "created_at" in payload:
        payload["created_at"] = None

    assert response.status_code == HTTPStatus.CREATED
    assert payload == {
        "nome_grupo": "Escola Estadual e Cordão de Samba Rock B Negão",
        "data_visita": "2024-10-15T14:30:00Z",
        "descricao": "Trampo técnico, mezzo aliche mezzo catupiry",
        "image_list": [
            "https://minha-bucket.s3.aws.com/foto1.jpg",
            "https://minha-bucket.s3.aws.com/foto2.jpg",
        ],
        "video_list": ["https://youtube.com/watch?v=exemplo"],
        "id": 2,
        "created_at": None,
    }


def test_read_visitas(client: TestClient):
    response = client.get("/")  # noqa: F811

    for item in response.json()["visitas"]:
        assert "id" in item
        assert "nome_grupo" in item
        assert "data_visita" in item
        assert "descricao" in item
        assert "image_list" in item
        assert "video_list" in item
        assert "created_at" in item

    assert response.status_code == HTTPStatus.OK


def test_read_visitas_com_o_payload(client: TestClient):
    response = client.get("/")  # noqa: F811
    payload = response.json()

    payload_limpo = {
        "visitas": [
            {k: v for k, v in visita.items() if k != "created_at"}
            for visita in payload["visitas"]
        ]
    }

    assert payload_limpo == {
        "visitas": [
            {
                "nome_grupo": "Grupo Escolar José Mojica Marins",
                "data_visita": "2024-10-15T14:30:00Z",
                "descricao": "Trampo técnico, mezzo aliche mezzo catupiry",
                "image_list": [
                    "https://minha-bucket.s3.aws.com/foto1.jpg",
                    "https://minha-bucket.s3.aws.com/foto2.jpg",
                ],
                "video_list": ["https://youtube.com/watch?v=exemplo"],
                "id": 1,
            },
            {
                "nome_grupo": "Escola Estadual e Cordão de Samba Rock B Negão",
                "data_visita": "2024-10-15T14:30:00Z",
                "descricao": "Trampo técnico, mezzo aliche mezzo catupiry",
                "image_list": [
                    "https://minha-bucket.s3.aws.com/foto1.jpg",
                    "https://minha-bucket.s3.aws.com/foto2.jpg",
                ],
                "video_list": ["https://youtube.com/watch?v=exemplo"],
                "id": 2,
            },
        ]
    }
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    ("visita_id", "expected_grupo", "should_error"),
    [
        (1, "Grupo Escolar José Mojica Marins", False),
        (2, "Escola Estadual e Cordão de Samba Rock B Negão", False),
        (3, "Escola Inexistente", True),
        (999, None, True),
    ],
)
def test_read_visita_by_id(
    visita_id: int, expected_grupo: str, should_error: bool
):
    if should_error:
        with pytest.raises(HTTPException) as excinfo:
            read_visita_by_id(visita_id)

        assert excinfo.value.status_code == HTTPStatus.NOT_FOUND
    else:
        response = read_visita_by_id(visita_id)
        assert response.nome_grupo == expected_grupo
        assert response.id == visita_id


def test_update_visita(client: TestClient):
    jasao = {
        "nome_grupo": "Escola Estadual e Cordão de Samba Rock B Negão "
        "E os seletores de frequência",
        "data_visita": "2024-10-15T14:30:00Z",
        "descricao": "Trampo técnico, mezzo aliche mezzo catupiry",
        "image_list": [
            "https://minha-bucket.s3.aws.com/foto1.jpg",
            "https://minha-bucket.s3.aws.com/foto2.jpg",
        ],
        "video_list": ["https://youtube.com/watch?v=exemplo"],
        "id": 2,
        "created_at": "",
    }

    response = client.put("/2", json=jasao)  # noqa: F811
    payload = response.json()

    payload_limpo = {k: v for k, v in payload.items() if k != "created_at"}

    assert response.status_code == HTTPStatus.OK
    assert payload_limpo == {
        "nome_grupo": "Escola Estadual e Cordão de Samba Rock B Negão "
        "e os Seletores de Frequência",
        "data_visita": "2024-10-15T14:30:00Z",
        "descricao": "Trampo técnico, mezzo aliche mezzo catupiry",
        "image_list": [
            "https://minha-bucket.s3.aws.com/foto1.jpg",
            "https://minha-bucket.s3.aws.com/foto2.jpg",
        ],
        "video_list": ["https://youtube.com/watch?v=exemplo"],
        "id": 2,
    }


def test_delete_visita(client: TestClient):
    response = client.delete("/2")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Visita deletada com sucesso!"}


def test_read_visita_nao_encontrada(client: TestClient):
    response = client.get("/-1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Visita não encontrada"}


def test_update_visita_nao_encontrada(client: TestClient):
    jasao = {
        "nome_grupo": "Escola Estadual e Cordão de Samba Rock B Negão "
        "E os seletores de frequência",
        "data_visita": "2024-10-15T14:30:00Z",
        "descricao": "Trampo técnico, mezzo aliche mezzo catupiry",
        "image_list": [
            "https://minha-bucket.s3.aws.com/foto1.jpg",
            "https://minha-bucket.s3.aws.com/foto2.jpg",
        ],
        "video_list": ["https://youtube.com/watch?v=exemplo"],
        "id": 2,
        "created_at": "",
    }

    response = client.put("/-1", json=jasao)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Visita não encontrada"}


def test_delete_visita_nao_encontrada(client: TestClient):
    response = client.delete("/-1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Visita não encontrada"}
