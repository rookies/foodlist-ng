#!/usr/bin/env python3
"""
This file implements create, read, update, and delete operations for database
objects.
"""
from typing import Optional
from sqlalchemy.orm import Session
from . import models, schemas, enums


def get_items(db: Session, order_by: enums.ItemOrderBy, order_direction: enums.OrderDirection, filters: Optional[list] = None):
    q = db.query(models.Item)

    if filters is not None:
        q = q.filter(*filters)

    if order_direction == enums.OrderDirection.DESC:
        q = q.order_by(getattr(models.Item, order_by.value).desc())
    else:
        q = q.order_by(getattr(models.Item, order_by.value))

    return q.all()


def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def get_item_by_id(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()


def delete_item_by_id(db: Session, id: int):
    db.query(models.Item).filter(models.Item.id == id).delete()
    db.commit()


def update_item_by_id(db: Session, id: int, **kwargs):
    db.query(models.Item).filter(models.Item.id == id).update(kwargs)
    db.commit()
