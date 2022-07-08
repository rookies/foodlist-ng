#!/usr/bin/env python3
"""
This file contains all database models.
"""
from datetime import datetime
from sqlalchemy import Column, Text, Integer, Date, Interval, Boolean, DateTime
from .database import Base


class Inventory(Base):
    __tablename__ = "foodlist_inventories"

    id = Column(Integer, primary_key=True)
    secret_key = Column(Text, index=True, nullable=False)
    shopping_notes = Column(Text, nullable=False)


class Item(Base):
    __tablename__ = "foodlist_items"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
    min_quantity = Column(Integer, nullable=False)
    temporary_additional_min_quantity = Column(Integer, nullable=False)
    best_before = Column(Date, nullable=True)
    expire_warning = Column(Interval, nullable=True)
    keep_if_zero = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    hidden_on_shopping = Column(Boolean, nullable=False)

    # TODO: reference to inventory

    @property
    def time_until_spoiled(self):
        if not self.best_before:
            return None
        return self.best_before - timezone.now().date()

    @property
    def spoiled(self):
        if not self.best_before:
            return False
        return (self.remainingTime < timedelta(0))

    @property
    def soon_spoiled(self):
        if not self.best_before:
            return False
        return (self.remainingTime < self.expire_warning)