"""Family model
"""
from datetime import datetime
from logging import getLogger

from anyblok import Declarations
from anyblok.column import (
    String,
    Text,
    Selection,
    DateTime,
    Integer
)
from anyblok.field import Function
from anyblok.relationship import Many2One

from anyblok_postgres.column import Jsonb


logger = getLogger(__name__)
Model = Declarations.Model
register = Declarations.register


@Declarations.register(Model.Product)
class Family:
    """Product.Family class
    """
    FAMILY_CODE = None
    family_schema = None
    template_schema = None
    item_schema = None

    id = Integer(label="Identifier", primary_key=True)
    create_date = DateTime(default=datetime.now, nullable=False)
    edit_date = DateTime(default=datetime.now, nullable=False,
                         auto_update=True)
    code = String(label="Family code", unique=True, nullable=False)
    name = String(label="Family name", max_length=256)
    description = Text(label="Family description")
    properties = Jsonb(label="Family properties")

    family_code = Selection(selections='get_family_codes')
    items = Function(fget="fget_items")

    @classmethod
    def get_family_codes(cls):
        return dict()

    def fget_items(self):
        """Returns a list of products instance from this family
        """
        return self.registry.InstrumentedList(
            set([i for t in self.templates for i in t.items]))

    @classmethod
    def create(cls, **kwargs):
        data = kwargs.copy()
        if cls.family_schema:
            sch = cls.family_schema(registry=cls.registry)
            data = sch.load(kwargs)
        return cls.insert(**data)

    @classmethod
    def query(cls, *args, **kwargs):
        query = super(Family, cls).query(*args, **kwargs)
        if cls.__registry_name__ != 'Model.Product.Family':
            query = query.filter(cls.family_code == cls.FAMILY_CODE)

        return query

    @classmethod
    def define_mapper_args(cls):
        mapper_args = super(Family, cls).define_mapper_args()
        if cls.__registry_name__ == 'Model.Product.Family':
            mapper_args.update({'polymorphic_on': cls.family_code})

        mapper_args.update({'polymorphic_identity': cls.FAMILY_CODE})
        return mapper_args

    def __str__(self):
        return "%s : %s" % (self.code, self.name)

    def __repr__(self):
        return "<Product.Family(code=%s, name=%s)>" % (
            self.code, self.name)


@register(Model.Product)
class Template:
    """Add family relationship to template
    """
    family = Many2One(label="Family",
                      model=Declarations.Model.Product.Family,
                      one2many='templates',
                      nullable=False)

    @classmethod
    def create(cls, family, **kwargs):
        data = kwargs.copy()
        if family.template_schema:
            sch = family.template_schema(registry=cls.registry)
            data = sch.load(kwargs, instances=dict(default=family))
        return cls.insert(family=family, **data)
