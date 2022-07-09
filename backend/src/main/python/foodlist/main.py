#!/usr/bin/env python3
"""
This is the main file of the foodlist-ng API Server.
"""
import uuid
import logging
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_
from sqlalchemy.orm import Session
from . import crud, schemas, enums, models
from .database import get_database

app = FastAPI(
    title="foodlist-ng",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)  # TODO: Fix this!
logger = logging.getLogger("foodlist.main")


@app.get("/items", response_model=List[schemas.Item])
async def list_items(order_by: enums.ItemOrderBy = enums.ItemOrderBy.id, order_direction: enums.OrderDirection = enums.OrderDirection.ASC, custom_filter: Optional[str] = None, db: Session = Depends(get_database)):
    """
    Lists all items.
    """
    filters = {
        "shopping": [
            or_(
                models.Item.quantity < models.Item.min_quantity,
                models.Item.temporary_additional_min_quantity > 0,
            ),
            models.Item.hidden_on_shopping == False,
        ],
    }
    return crud.get_items(db, order_by, order_direction, filters.get(custom_filter, []))


@app.post("/items", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_database)):
    """
    Creates a new item.
    """
    return crud.create_item(db, item)


@app.delete("/items/{id}")
async def delete_item(id: int, db: Session = Depends(get_database)):
    """
    Deletes the item with the given ID.
    """
    crud.delete_item_by_id(db, id)


@app.patch("/items/{id}", response_model=schemas.Item)
async def update_item(id: int, item: schemas.ItemUpdate, db: Session = Depends(get_database)):
    """
    Updates the item with the given ID.
    """
    crud.update_item_by_id(db, id, **item.dict(exclude_unset=True))
    return crud.get_item_by_id(db, id)


@app.post("/items/{id}/tags/{tag}", response_model=schemas.Item)
async def add_item_tag(id: int, tag: str, db: Session = Depends(get_database)):
    """
    Adds a tag to the item with the given ID.
    """
    crud.create_item_tag(db, id, tag)
    return crud.get_item_by_id(db, id)


@app.delete("/items/{id}/tags/{tag}", response_model=schemas.Item)
async def add_item_tag(id: int, tag: str, db: Session = Depends(get_database)):
    """
    Removes a tag from the item with the given ID.
    """
    crud.delete_item_tag(db, id, tag)
    return crud.get_item_by_id(db, id)
