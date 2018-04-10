from marshmallow import Schema, fields, validates_schema, ValidationError

from anyblok import Declarations

from anyblok_marshmallow import ModelSchema
from anyblok_marshmallow.fields import Nested


register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


class ShoeFamilySchemaProperties(Schema):
    brands = fields.List(fields.Str())
    sizes = fields.List(fields.Str())
    colors = fields.List(fields.Str())
    styles = fields.List(fields.Str())
    genres = fields.List(fields.Str())

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)


class ShoeFamilySchema(ModelSchema):

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)

    class Meta:
        model = "Model.Product.Family"

    properties = Nested(ShoeFamilySchemaProperties(partial=True))


@register(Model.Product.Family, tablename=Model.Product.Family)
class ShoeFamilyTest(Model.Product.Family):
    family_schema = ShoeFamilySchema
