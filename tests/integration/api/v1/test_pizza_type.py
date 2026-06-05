from decimal import Decimal
from uuid import uuid4

import pytest

import app.api.v1.endpoints.dough.crud as dough_crud
import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud

from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema

from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_pizza_type_create_read_delete(db):

    # Arrange
    dough = DoughCreateSchema(
        name=f'test_dough_{uuid4()}',
        price=Decimal('1.50'),
        description='integration test dough',
        stock=10,
    )

    created_dough = dough_crud.create_dough(dough, db)

    pizza_type = PizzaTypeCreateSchema(
        name=f'pizza_{uuid4()}',
        price=12.50,
        description='integration test pizza',
        dough_id=created_dough.id,
    )

    number_before = len(pizza_type_crud.get_all_pizza_types(db))

    # Act
    created_pizza = pizza_type_crud.create_pizza_type(pizza_type, db)

    # Assert
    all_pizzas = pizza_type_crud.get_all_pizza_types(db)
    assert len(all_pizzas) == number_before + 1

    read_pizza = pizza_type_crud.get_pizza_type_by_id(
        created_pizza.id,
        db,
    )

    assert read_pizza.id == created_pizza.id
    assert read_pizza.name == pizza_type.name
    assert read_pizza.description == pizza_type.description

    # Cleanup
    pizza_type_crud.delete_pizza_type_by_id(created_pizza.id, db)
    dough_crud.delete_dough_by_id(created_dough.id, db)

    deleted = pizza_type_crud.get_pizza_type_by_id(
        created_pizza.id,
        db,
    )

    assert deleted is None