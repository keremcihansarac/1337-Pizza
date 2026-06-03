from decimal import Decimal
from uuid import uuid4

import pytest

import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_dough_create_read_delete(db):
    new_dough_name = f'test_dough_{uuid4()}'
    expected_stock = 10
    number_of_doughs_before = len(dough_crud.get_all_doughs(db))

    # Arrange: Instantiate a new dough object
    dough = DoughCreateSchema(
        name=new_dough_name,
        price=Decimal('1.11'),
        description='test description',
        stock=expected_stock,
    )

    # Act: Add dough to database
    db_dough = dough_crud.create_dough(dough, db)
    created_dough_id = db_dough.id

    # Assert: One more dough in database
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before + 1

    # Act: Re-read dough from database
    read_dough = dough_crud.get_dough_by_id(created_dough_id, db)

    # Assert: Correct dough was stored in database
    assert read_dough.id == created_dough_id
    assert read_dough.name == new_dough_name
    assert read_dough.price == Decimal('1.11')
    assert read_dough.description == 'test description'
    assert read_dough.stock == 10 # noqa: PLR2004

    # Act: Delete dough
    dough_crud.delete_dough_by_id(created_dough_id, db)

    # Assert: Correct number of doughs in database after deletion
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before

    # Assert: Correct dough was deleted from database
    deleted_dough = dough_crud.get_dough_by_id(created_dough_id, db)
    assert deleted_dough is None