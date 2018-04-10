"""Family model
"""
from logging import getLogger

from marshmallow.exceptions import ValidationError

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
    family_schema = None
    template_schema = None
    item_schema = None

    code = String(label="Family code", unique=True, nullable=False)
    name = String(label="Family name")
    description = Text(label="Family description")
    properties = Jsonb(label="Family properties")

    @classmethod
    def create(cls, **kwargs):
        if cls.family_schema:
            sch = cls.family_schema(registry=cls.registry)
            errors = sch.validate(kwargs)
            if errors:
                raise ValidationError(errors)
        return cls.insert(**kwargs)

    def __str__(self):
        return "%s : %s" % (self.code, self.name)

    def __repr__(self):
        return "<Product.Family(code=%s, name=%s)>" % (
            self.code, self.name)
