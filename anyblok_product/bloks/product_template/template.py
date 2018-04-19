"""Template model
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
class Template(Mixin.IdColumn, Mixin.TrackModel):
    """Template class
    """
    code = String(label="Template code", unique=True, nullable=False)
    name = String(label="Template name")
    description = Text(label="Template description")
    properties = Jsonb(label="Template properties")

    def __str__(self):
        return "%s : %s" % (self.sku, self.name)

    def __repr__(self):
        return "<Template(sku=%s, name=%s)>" % (
            self.sku, self.name)
