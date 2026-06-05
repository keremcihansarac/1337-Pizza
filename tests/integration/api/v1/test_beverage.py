from uuid import uuid4

import pytest

import app.api.v1.endpoints.beverage.crud as beverage_crud
from app.api.v1.endpoints.beverage.schemas import BeverageCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_beverage_create_read_delete(db):
    new_beverage_name = f"test_beverage_{uuid4()}"
    expected_stock = 20

    number_before = len(beverage_crud.get_all_beverages(db))

    # Arrange
    beverage = BeverageCreateSchema(
        name=new_beverage_name,
        price=2.49,
        description="test beverage",
        stock=expected_stock,
    )

    # Act
    db_beverage = beverage_crud.create_beverage(beverage, db)
    beverage_id = db_beverage.id

    # Assert
    beverages = beverage_crud.get_all_beverages(db)
    assert len(beverages) == number_before + 1

    # Act
    read_beverage = beverage_crud.get_beverage_by_id(beverage_id, db)

    # Assert
    assert read_beverage.id == beverage_id
    assert read_beverage.name == new_beverage_name
    assert read_beverage.price == 2.49
    assert read_beverage.description == "test beverage"
    assert read_beverage.stock == expected_stock

    # Act
    beverage_crud.delete_beverage_by_id(beverage_id, db)

    # Assert
    beverages = beverage_crud.get_all_beverages(db)
    assert len(beverages) == number_before

    deleted = beverage_crud.get_beverage_by_id(beverage_id, db)
    assert deleted is None