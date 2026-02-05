from datetime import datetime, timedelta, timezone
from http import HTTPStatus

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from museu_scaffoldo.modules.visitas import routers
from tests.utils.time_assertions import assert_iso_datetime_close

app = FastAPI()
app.include_router(routers.router_visita)


@pytest.fixture
def client():
    return TestClient(app)


def test_create_visita(client: TestClient, freezer):
    freezer.move_to(datetime(2026, 2, 5, 12, 0, 0, tzinfo=timezone.utc))

    jasao = {
        "nome_grupo": "Grupo Escolar José Mojica Marins",
        "data_visita": "2024-10-15T14:30:00",
        "descricao": "Trampo técnico, mezzo aliche mezzo catupiry",
        "image_list": [
            "https://minha-bucket.s3.aws.com/foto1.jpg",
            "https://minha-bucket.s3.aws.com/foto2.jpg",
        ],
        "video_list": ["https://youtube.com/watch?v=exemplo"],
    }

    frozen_now = datetime.now(timezone.utc)

    response = client.post("/", json=jasao)  # noqa: F811
    payload = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert_iso_datetime_close(
        payload["created_at"],
        frozen_now,
        delta=timedelta(milliseconds=500),  # putz!!
    )


# def test_read_visitas(client: TestClient):
#     response = client.get("/")  # noqa: F811
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {
#         "visitas": [
#             {
#                 "nome_grupo": "Grupo Escolar José Mojica Marins",
#                 "data_visita": "2024-10-15T14:30:00",
#                 "descricao": "Trampo técnico, mezzo aliche mezzo catupiry",
#                 "image_list": [
#                     "https://minha-bucket.s3.aws.com/foto1.jpg",
#                     "https://minha-bucket.s3.aws.com/foto2.jpg",
#                 ],
#                 "video_list": ["https://youtube.com/watch?v=exemplo"],
#                 "id": 1,
#                 "created_at": frozen_time,
#             }
#         ]
#     }
