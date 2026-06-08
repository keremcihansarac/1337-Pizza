from uuid import uuid4

import pytest

import app.api.v1.endpoints.beverage.crud as beverage_crud
from app.api.v1.endpoints.beverage.schemas import BeverageCreateSchema
from app.api.v1.endpoints.order.stock_logic import stock_beverage_crud

from app.database.connection import SessionLocal

EXPECTED_STOCK = 5


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_beverage_is_available_and_change_stock(db):
    beverage = beverage_crud.create_beverage(
        BeverageCreateSchema(
            name=f'test_beverage_{uuid4()}',
            price=2.5,
            description='test beverage',
            stock=10,
        ),
        db,
    )

    assert stock_beverage_crud.beverage_is_available(
        beverage.id,
        5,
        db,
    )

    result = stock_beverage_crud.change_stock_of_beverage(
        beverage.id,
        -5,
        db,
    )

    assert result is True

    updated = beverage_crud.get_beverage_by_id(
        beverage.id,
        db,
    )

    assert updated.stock == EXPECTED_STOCK

    beverage_crud.delete_beverage_by_id(
        beverage.id,
        db,
    )