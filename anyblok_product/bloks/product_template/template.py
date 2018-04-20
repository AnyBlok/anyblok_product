"""Template model
"""
from datetime import datetime
from logging import getLogger

from anyblok import Declarations
from anyblok.column import (
    String,
    Text,
    DateTime,
    Integer
)

from anyblok.relationship import Many2One

from anyblok_postgres.column import Jsonb


logger = getLogger(__name__)
Model = Declarations.Model
register = Declarations.register


@Declarations.register(Model.Product)
class Template:
    """Template class
    """
    id = Integer(label="Identifier", primary_key=True)
    create_date = DateTime(default=datetime.now, nullable=False)
    edit_date = DateTime(default=datetime.now, nullable=False,
                         auto_update=True)
    code = String(label="Template code", unique=True, nullable=False)
    name = String(label="Template name")
    description = Text(label="Template description")
    properties = Jsonb(label="Template properties")

    def __str__(self):
        return "%s : %s" % (self.code, self.name)

    def __repr__(self):
        return "<Template(code=%s, name=%s)>" % (
            self.code, self.name)


@register(Model.Product)
class Item:
    """Add template relationship to item
    """
    template = Many2One(label="Template",
                        model=Declarations.Model.Product.Template,
                        one2many='items',
                        nullable=False)

    @classmethod
    def create(cls, template, **kwargs):
        data = kwargs.copy()
        if template.family.item_schema:
            sch = template.family.item_schema(registry=cls.registry)
            data = sch.load(kwargs, instances=dict(default=template.family))
        return cls.insert(template=template, **data)
