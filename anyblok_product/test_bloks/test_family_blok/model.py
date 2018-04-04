from marshmallow import Schema

from anyblok import Declarations
from anyblok.column import Integer

from anyblok_marshmallow import ModelSchema
from anyblok_marshmallow.fields import Nested

register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


class ShoeFamilySchemaProperties(Schema):
    pass

class ShoeFamilySchema(ModelSchema):

    class Meta:
        model = "Model.Product.Family"

    properties = Nested(ShoeFamilySchemaProperties)


@register(Model.Product.Family, tablename=Model.Product.Family)
class ShoeFamilyTest(Model.Product.Family):
    family_schema = ShoeFamilySchema
