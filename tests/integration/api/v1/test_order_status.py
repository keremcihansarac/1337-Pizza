from uuid import uuid4

import pytest

import app.api.v1.endpoints.order.crud as order_crud
import app.api.v1.endpoints.user.crud as user_crud

from app.api.v1.endpoints.order.schemas import OrderCreateSchema
from app.api.v1.endpoints.user.schemas import UserCreateSchema
from app.database.connection import SessionLocal
from app.database.models import OrderStatus


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_order_status_filter(db):
    user = user_crud.create_user(
        UserCreateSchema(username=f'test_user_{uuid4()}'),
        db,
    )
    order = order_crud.create_order(
        OrderCreateSchema(
            user_id=user.id,
            address={
                'street': 'Test Street',
                'post_code': '64289',
                'house_number': 1,
                'country': 'Germany',
                'town': 'Darmstadt',
                'first_name': 'Kashf',
                'last_name': 'Malik',
            },
        ),
        db,
    )

    try:
        transmitted_orders = order_crud.get_all_orders(db, OrderStatus.TRANSMITTED)
        assert any(entity.id == order.id for entity in transmitted_orders)
        assert all(entity.order_status == OrderStatus.TRANSMITTED for entity in transmitted_orders)

        updated_order = order_crud.update_order_status(order, OrderStatus.PREPARING, db)
        assert updated_order.order_status == OrderStatus.PREPARING

        preparing_orders = order_crud.get_all_orders(db, OrderStatus.PREPARING)
        assert any(entity.id == order.id for entity in preparing_orders)
        assert all(entity.order_status == OrderStatus.PREPARING for entity in preparing_orders)

        transmitted_orders = order_crud.get_all_orders(db, OrderStatus.TRANSMITTED)
        assert all(entity.id != order.id for entity in transmitted_orders)
    finally:
        order_crud.delete_order_by_id(order.id, db)
        user_crud.delete_user_by_id(user.id, db)
