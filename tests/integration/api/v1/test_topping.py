from uuid import uuid4

import pytest

import app.api.v1.endpoints.topping.crud as topping_crud
from app.api.v1.endpoints.topping.schemas import ToppingCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_topping_create_read_delete(db):
    new_topping_name = f"test_topping_{uuid4()}"
    expected_stock = 15

    number_before = len(topping_crud.get_all_toppings(db))

    # Arrange
    topping = ToppingCreateSchema(
        name=new_topping_name,
        price=1.99,
        description="test topping",
        stock=expected_stock,
    )

    # Act
    db_topping = topping_crud.create_topping(topping, db)
    topping_id = db_topping.id

    # Assert
    toppings = topping_crud.get_all_toppings(db)
    assert len(toppings) == number_before + 1

    # Act
    read_topping = topping_crud.get_topping_by_id(topping_id, db)

    # Assert
    assert read_topping.id == topping_id
    assert read_topping.name == new_topping_name
    assert read_topping.price == 1.99
    assert read_topping.description == "test topping"
    assert read_topping.stock == expected_stock

    # Act
    topping_crud.delete_topping_by_id(topping_id, db)

    # Assert
    toppings = topping_crud.get_all_toppings(db)
    assert len(toppings) == number_before

    deleted = topping_crud.get_topping_by_id(topping_id, db)
    assert deleted is None