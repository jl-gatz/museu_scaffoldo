from http import HTTPStatus


def test_create_equipamento(client, sample_equipamento_data):
    response = client.post("/", json=sample_equipamento_data)
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["id"] == 1
    assert data["marca"] == "IBM"
    assert data["modelo"] == "HAL 9000"
    assert data["qr_code"] == "AB1234"


def test_read_equipamentos_empty(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"equipamentos": []}


def test_read_equipamentos_after_create(client, sample_equipamento_data):
    # Cria um equipamento
    client.post("/", json=sample_equipamento_data)
    # Agora lista
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data["equipamentos"]) == 1
    equip = data["equipamentos"][0]
    assert equip["id"] == 1
    assert equip["marca"] == "IBM"


def test_read_equipamento_by_id(client, sample_equipamento_data):
    client.post("/", json=sample_equipamento_data)
    response = client.get("/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == 1


def test_read_equipamento_by_id_not_found(client):
    response = client.get("/999")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_search_equipamentos_by_termo(client, sample_equipamento_data):
    client.post("/", json=sample_equipamento_data)
    response = client.get("/search/IBM")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data["equipamentos"]) == 1


def test_update_equipamento(client, sample_equipamento_data):
    # Cria
    create_resp = client.post("/", json=sample_equipamento_data)
    equip_id = create_resp.json()["id"]
    # Atualiza
    update_data = sample_equipamento_data.copy()
    update_data["marca"] = "Updated"
    response = client.put(f"/{equip_id}", json=update_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["marca"] == "Updated"


def test_delete_equipamento(client, sample_equipamento_data):
    client.post("/", json=sample_equipamento_data)
    response = client.delete("/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Equipamento removido com sucesso"}
    # Verifica se foi deletado
    get_resp = client.get("/1")
    assert get_resp.status_code == HTTPStatus.NOT_FOUND
