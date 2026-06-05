from uuid import uuid4

import pytest

import app.api.v1.endpoints.order.crud as order_crud
import app.api.v1.endpoints.user.crud as user_crud

from app.api.v1.endpoints.order.schemas import OrderCreateSchema
from app.api.v1.endpoints.user.schemas import UserCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_order_create_read_update_delete(db):
    # Create user first
    username = f'test_user_{uuid4()}'
    user = user_crud.create_user(
        UserCreateSchema(username=username),
        db,
    )

    number_before = len(order_crud.get_all_orders(db))

    # Create order
    order_schema = OrderCreateSchema(
        user_id=user.id,
        address={
            'street': 'Test Street',
            'house_number': '1',
            'zip_code': '64289',
            'city': 'Darmstadt',
        },
    )

    db_order = order_crud.create_order(order_schema, db)
    order_id = db_order.id

    # Read
    orders = order_crud.get_all_orders(db)
    assert len(orders) == number_before + 1

    read_order = order_crud.get_order_by_id(order_id, db)

    assert read_order.id == order_id
    assert read_order.user_id == user.id

    # Update status
    updated_order = order_crud.update_order_status(
        read_order,
        read_order.order_status,
        db,
    )

    assert updated_order.id == order_id

    # Delete
    order_crud.delete_order_by_id(order_id, db)

    orders = order_crud.get_all_orders(db)
    assert len(orders) == number_before

    deleted_order = order_crud.get_order_by_id(order_id, db)

    assert deleted_order is None

    # Cleanup user
    user_crud.delete_user_by_id(user.id, db)