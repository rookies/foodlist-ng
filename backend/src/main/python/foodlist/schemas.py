#!/usr/bin/env python3
"""
This file contains the schemas used for API requests and responses.
"""
import uuid
from typing import Optional
from datetime import date, datetime, timedelta
from pydantic import BaseModel, conint


class ItemBase(BaseModel):
    """Base schema for an item."""

    quantity: conint(ge=0) = 1
    min_quantity: conint(ge=0) = 1
    temporary_additional_min_quantity: conint(ge=0) = 0
    best_before: Optional[date]
    expire_warning: Optional[timedelta] = timedelta(days=7)
    keep_if_zero: bool = True  # TODO: Always true?
    hidden_on_shopping: bool = False


class ItemCreate(ItemBase):
    """Schema for creating an item."""

    name: str


class ItemUpdate(ItemBase):
    """Schema for updating an item."""

    name: Optional[str]


class Item(ItemBase):
    """Schema for returning an item."""

    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    time_until_expired: Optional[timedelta]
    expired: bool
    soon_expired: bool

    class Config:
        """Configuration for the schema."""

        orm_mode = True
