import uuid
from typing import List, TypeVar, Annotated

from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from sqlalchemy.orm import Session
import logging

import app.api.v1.endpoints.dough.crud as dough_crud
import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
import app.api.v1.endpoints.topping.crud as topping_crud
from app.api.v1.endpoints.dough.schemas import DoughSchema
from app.api.v1.endpoints.pizza_type.schemas import \
    JoinedPizzaTypeQuantitySchema, \
    PizzaTypeSchema, \
    PizzaTypeCreateSchema, \
    PizzaTypeToppingQuantityCreateSchema
from app.database.connection import SessionLocal

router = APIRouter()

pizza_type_not_found = 'Pizza type not found'


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('', response_model=<L>ist[PizzaTypeSchema], tags=['pizza_type'])
def get_all_pizza_types(db: Annotated[Session, Depends(get_db)]):
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    return pizza_types


@router.post('', response_model=PizzaTypeSchema, tags=['pizza_type'])
def create_pizza_type(
        pizza_type: PizzaTypeCreateSchema, request: Request,
        response: Response, db: Annotated[Session, Depends(get_db)],
):
    pizza_type_found = pizza_type_crud.get_pizza_type_by_name(pizza_type.name, db)

    if pizza_type_found:
        logging.warning('Could not create pizza type with name %s because it already exists', pizza_type.name)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    dough = dough_crud.get_dough_by_id(pizza_type.dough_id, db)
    if not dough:
        logging.warning(
            'Could not create pizza type %s because dough %s was not found',
            pizza_type.name,
            pizza_type.dough_id,
        )
        raise HTTPException(status_code=404, detail=pizza_type_not_found)

    new_pizza_type = pizza_type_crud.create_pizza_type(pizza_type, db)
    logging.info(
        'Created pizza type with id %s, name %s and dough %s',
        new_pizza_type.id,
        pizza_type.name,
        pizza_type.dough_id,
    )
    response.status_code = status.HTTP_201_CREATED
    return new_pizza_type


@router.put('/{pizza_type_id}', response_model=PizzaTypeSchema, tags=['pizza_type'])
def update_pizza_type(
        pizza_type_id: uuid.UUID,
        changed_pizza_type: PizzaTypeCreateSchema,
        request: Request,
        response: Response,
        db: Annotated[Session, Depends(get_db)],
):
    pizza_type_found = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    updated_pizza_type = None

    if pizza_type_found:
        if pizza_type_found.name == changed_pizza_type.name:
            pizza_type_crud.update_pizza_type(pizza_type_found, changed_pizza_type, db)
            logging.info('Updated pizza type with id %s and name %s', pizza_type_id, changed_pizza_type.name)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            pizza_type_name_found = pizza_type_crud.get_pizza_type_by_name(changed_pizza_type.name, db)
            if pizza_type_name_found:
                logging.warning(
                    'Could not update pizza type %s to name %s because the name already exists',
                    pizza_type_id,
                    changed_pizza_type.name,
                )
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)
            else:
                logging.warning('Could not update pizza type %s because it was not found', pizza_type_id)
                raise HTTPException(status_code=404, detail=pizza_type_not_found)
    else:
        raise HTTPException(status_code=404, detail=pizza_type_not_found)

    return updated_pizza_type


@router.get('/{pizza_type_id}', response_model=PizzaTypeSchema, tags=['pizza_type'])
def get_pizza_type(
        pizza_type_id: uuid.UUID,
        db: Annotated[Session, Depends(get_db)],
):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    if not pizza_type:
        logging.warning(
            'Could not add topping %s to pizza type %s because the pizza type was not found',
            topping_quantity.topping_id,
            pizza_type_id,
        )
        raise HTTPException(status_code=404, detail=pizza_type_not_found)


@router.delete('/{pizza_type_id}', response_model=None, tags=['pizza_type'])
def delete_pizza_type(pizza_type_id: uuid.UUID,
                      db: Annotated[Session, Depends(get_db)],
                      ):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)

    if not pizza_type:
        raise HTTPException(status_code=404, detail=pizza_type_not_found)

    pizza_type_crud.delete_pizza_type_by_id(pizza_type_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Due to mypy error, this workaround is needed for Union
# see pull request https://github.com/python/mypy/pull/8779
# should be fixed in near future
MyPyEitherItem = TypeVar(
    'MyPyEitherItem',
    List[PizzaTypeToppingQuantityCreateSchema],
    List[JoinedPizzaTypeQuantitySchema],
    None,
)


@router.get(
    '/{pizza_type_id}/toppings',
    response_model=MyPyEitherItem,
    tags=['pizza_type'],
)
def get_pizza_type_toppings(
        pizza_type_id: uuid.UUID,
        response: Response,
        db: Annotated[Session, Depends(get_db)],
        join: bool = False,
):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)

    if not pizza_type:
        raise HTTPException(status_code=404, detail=pizza_type_not_found)

    toppings = pizza_type.toppings
    if join:
        toppings = pizza_type_crud.get_joined_topping_quantities_by_pizza_type(pizza_type.id, db)

    return toppings


@router.post(
    '/{pizza_type_id}/toppings',
    response_model=PizzaTypeToppingQuantityCreateSchema,
    status_code=status.HTTP_201_CREATED,
    tags=['pizza_type'],
)
def create_pizza_type_topping(
        pizza_type_id: uuid.UUID,
        topping_quantity: PizzaTypeToppingQuantityCreateSchema,
        request: Request,
        response: Response,
        db: Annotated[Session, Depends(get_db)],
):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    if not pizza_type:
        raise HTTPException(status_code=404, detail=pizza_type_not_found)

    if not topping_crud.get_topping_by_id(topping_quantity.topping_id, db):
        logging.warning(
            'Could not add topping %s to pizza type %s because the topping was not found',
            topping_quantity.topping_id,
            pizza_type_id,
        )
        raise HTTPException(status_code=404, detail=pizza_type_not_found)

    topping_quantity_found = pizza_type_crud.get_topping_quantity_by_id(pizza_type_id, topping_quantity.topping_id, db)
    if topping_quantity_found:
        logging.warning(
            'Could not add topping %s to pizza type %s because the relation already exists',
            topping_quantity.topping_id,
            pizza_type_id,
        )
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    new_topping_quantity = pizza_type_crud.create_topping_quantity(pizza_type, topping_quantity, db)
    logging.info(
        'Added topping %s with quantity %s to pizza type %s',
        topping_quantity.topping_id,
        topping_quantity.quantity,
        pizza_type_id,
    )
    return new_topping_quantity


@router.get(
    '/{pizza_type_id}/dough',
    response_model=DoughSchema,
    tags=['pizza_type'],
)
def get_pizza_type_dough(
        pizza_type_id: uuid.UUID,
        response: Response,
        db: Annotated[Session, Depends(get_db)],
):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)

    if not pizza_type:
        raise HTTPException(status_code=404, detail=pizza_type_not_found)

    dough = pizza_type.dough

    return dough
