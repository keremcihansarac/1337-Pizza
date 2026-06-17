import logging
import uuid
from typing import List, Annotated

from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from sqlalchemy.orm import Session

import app.api.v1.endpoints.beverage.crud as beverage_crud
from app.api.v1.endpoints.beverage.schemas import BeverageSchema, BeverageCreateSchema, BeverageListItemSchema
from app.database.connection import SessionLocal

beverage_not_found = 'Item not found'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get('', response_model=List[BeverageListItemSchema], tags=['beverage'])
def get_all_beverages(db: Annotated[Session, Depends(get_db)]):
    beverages = beverage_crud.get_all_beverages(db)
    return beverages


@router.post('', response_model=BeverageSchema, status_code=status.HTTP_201_CREATED, tags=['beverage'])
def create_beverage(beverage: BeverageCreateSchema,
                    request: Request,
                    db: Annotated[Session, Depends(get_db)]):
    beverage_found = beverage_crud.get_beverage_by_name(beverage.name, db)

    if beverage_found:
        logging.warning('Beverage creation failed: name %s already exists', beverage.name)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    new_beverage = beverage_crud.create_beverage(beverage, db)
    logging.info(
        'Beverage created: id=%s name=%s price=%s stock=%s',
        new_beverage.id,
        new_beverage.name,
        new_beverage.price,
        new_beverage.stock,
    )
    return new_beverage


@router.put('/{beverage_id}', response_model=BeverageSchema, tags=['beverage'])
def update_beverage(
        beverage_id: uuid.UUID,
        changed_beverage: BeverageCreateSchema,
        request: Request,
        response: Response,
        db: Annotated[Session, Depends(get_db)],
):
    beverage_found = beverage_crud.get_beverage_by_id(beverage_id, db)

    if beverage_found:
        if beverage_found.name == changed_beverage.name:
            beverage_crud.update_beverage(beverage_found, changed_beverage, db)
            logging.info(
                'Beverage updated: id=%s name=%s price=%s stock=%s',
                beverage_id,
                changed_beverage.name,
                changed_beverage.price,
                changed_beverage.stock,
            )
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            beverage_name_found = beverage_crud.get_beverage_by_name(changed_beverage.name, db)
            if beverage_name_found:
                logging.warning(
                    'Beverage update failed: id=%s cannot be renamed to existing name %s',
                    beverage_id,
                    changed_beverage.name,
                )
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)
            else:
                updated_beverage = beverage_crud.create_beverage(changed_beverage, db)
                response.status_code = status.HTTP_201_CREATED
                logging.info(
                    'Beverage update created replacement: requested_id=%s new_id=%s name=%s',
                    beverage_id,
                    updated_beverage.id,
                    updated_beverage.name,
                )
    else:
        logging.warning('Beverage update failed: id=%s not found', beverage_id)
        raise HTTPException(status_code=404, detail=beverage_not_found)

    return updated_beverage


@router.get('/{beverage_id}', response_model=BeverageSchema, tags=['beverage'])
def get_beverage(
        beverage_id: uuid.UUID,
        db: Annotated[Session, Depends(get_db)],
):
    beverage = beverage_crud.get_beverage_by_id(beverage_id, db)

    if not beverage:
        raise HTTPException(status_code=404, detail=beverage_not_found)

    return beverage


@router.delete('/{beverage_id}', response_model=None, tags=['beverage'])
def delete_beverage(
        beverage_id: uuid.UUID,
        db: Annotated[Session, Depends(get_db)]):
    beverage = beverage_crud.get_beverage_by_id(beverage_id, db)

    if not beverage:
        raise HTTPException(status_code=404, detail=beverage_not_found)

    beverage_crud.delete_beverage_by_id(beverage_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
