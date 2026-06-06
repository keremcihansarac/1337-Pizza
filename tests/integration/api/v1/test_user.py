from uuid import uuid4

import pytest

import app.api.v1.endpoints.user.crud as user_crud
from app.api.v1.endpoints.user.schemas import UserCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_user_create_read_update_delete(db):
    username = f'test_user_{uuid4()}'

    number_before = len(user_crud.get_all_users(db))

    # Arrange
    user = UserCreateSchema(
        username=username,
    )

    # Act
    db_user = user_crud.create_user(user, db)
    user_id = db_user.id

    # Assert
    users = user_crud.get_all_users(db)
    assert len(users) == number_before + 1

    read_user = user_crud.get_user_by_id(user_id, db)

    assert read_user.id == user_id
    assert read_user.username == username

    # Update
    updated_username = f'updated_{uuid4()}'

    changed_user = UserCreateSchema(
        username=updated_username,
    )

    user_crud.update_user(read_user, changed_user, db)

    updated_user = user_crud.get_user_by_id(user_id, db)

    assert updated_user.username == updated_username

    # Delete
    user_crud.delete_user_by_id(user_id, db)

    users = user_crud.get_all_users(db)
    assert len(users) == number_before

    deleted_user = user_crud.get_user_by_id(user_id, db)

    assert deleted_user is None