"""Product model
"""
from datetime import datetime
from logging import getLogger

from anyblok import Declarations
from anyblok.column import (
    DateTime,
    String,
    Integer
)

from anyblok_postgres.column import Jsonb


logger = getLogger(__name__)
Model = Declarations.Model
Mixin = Declarations.Mixin


@Declarations.register(Mixin)
class IdColumn:
    """ id primary key mixin
    """
    id = Integer(label="Identifier", primary_key=True)


@Declarations.register(Mixin)
class TrackModel:
    """ A mixin to store record creation and edition date
    """
    create_date = DateTime(default=datetime.now, nullable=False)
    edit_date = DateTime(default=datetime.now, nullable=False,
                         auto_update=True)


@Declarations.register(Declarations.Model)
class Product:
    """Namespace for product related models"""


@Declarations.register(Model.Product)
class Item(IdColumn, TrackModel):
    """Product.Item class
    """
    sku = String(label="Item sku", unique=True, nullable=True)
    name = String(label="Item name")
    description = String(label="Item description")
    properties = Jsonb(label="Item properties")

    def __str__(self):
        return "%s : %s" % (self.sku, self.name)

    def __repr__(self):
        return "<Product.Item(sku=%s, name=%s)>" % (
            self.sku, self.name)
