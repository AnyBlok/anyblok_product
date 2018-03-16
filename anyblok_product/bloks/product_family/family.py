"""Family model
"""
from logging import getLogger

from anyblok import Declarations
from anyblok.column import (
    String,
    Text,
)

from anyblok_postgres.column import Jsonb


logger = getLogger(__name__)
Model = Declarations.Model
Mixin = Declarations.Mixin


@Declarations.register(Model.Product)
class Family(Mixin.IdColumn, Mixin.TrackModel):
    """Product.Family class
    """
    code = String(label="Family code", unique=True, nullable=True)
    name = String(label="Family name")
    description = String(label="Family description")
    properties = Jsonb(label="Family properties")

    def __str__(self):
        return "%s : %s" % (self.code, self.name)

    def __repr__(self):
        return "<Product.Family(code=%s, name=%s)>" % (
            self.code, self.name)
