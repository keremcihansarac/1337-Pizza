from uuid import uuid4
import app.api.v1.endpoints.dough.crud as dough_crud
import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
import app.api.v1.endpoints.topping.crud as topping_crud
from app.api.v1.endpoints.order.stock_logic import stock_ingredients_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema
from app.api.v1.endpoints.topping.schemas import ToppingCreateSchema
from app.database.connection import SessionLocal



def create_test_pizza_setup(db):
    dough = dough_crud.create_dough(
        DoughCreateSchema(
            name=f'dough_{uuid4()}',
            price=2.0,
            description='test',
            stock=10,
        ),
        db,
    )

    topping = topping_crud.create_topping(
        ToppingCreateSchema(
            name=f'topping_{uuid4()}',
            price=1.0,
            description='test',
            stock=10,
        ),
        db,
    )

    pizza = pizza_type_crud.create_pizza_type(
        PizzaTypeCreateSchema(
            name=f'pizza_{uuid4()}',
            price=10.0,
            description='test',
            dough_id=dough.id,
            toppings=[
                {
                    'topping_id': topping.id,
                    'quantity': 2,
                },
            ],
        ),
        db,
    )
    return pizza





def test_ingredients_are_available():
    db = SessionLocal()


    pizza = create_test_pizza_setup(db)

    assert stock_ingredients_crud.ingredients_are_available(pizza)

    db.close()


def test_reduce_and_increase_stock():
    db = SessionLocal()

    expected_stock_after_reduce = 9
    expected_stock_after_increase = 10


    pizza = create_test_pizza_setup(db)

    stock_ingredients_crud.reduce_stock_of_ingredients(pizza, db)
    assert pizza.dough.stock == expected_stock_after_reduce

    stock_ingredients_crud.increase_stock_of_ingredients(pizza, db)
    assert pizza.dough.stock == expected_stock_after_increase

    db.close()