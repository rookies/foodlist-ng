#!/usr/bin/env python3
"""
This file contains enums used e.g. by database models.
"""
import enum
from . import schemas


class OrderDirection(str, enum.Enum):
    DESC = "desc"
    ASC = "asc"


ItemOrderBy = enum.Enum("ItemOrderBy", {v: v for v in [
    "id",
    "name",
    "quantity",
    "min_quantity",
    "temporary_additional_min_quantity",
    "best_before",
    "created_at",
    "updated_at",
]})
