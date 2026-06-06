from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_all_users_router():
    response = client.get('/v1/user')

    assert response.status_code == 200


def test_get_user_not_found():
    response = client.get(
        '/v1/user/00000000-0000-0000-0000-000000000000',
    )

    assert response.status_code == 404