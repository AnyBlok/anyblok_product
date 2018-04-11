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

    class Meta:
        model = "Model.Product.Family"

    properties = Nested(ShoeFamilySchemaProperties(partial=True))


class ShoeTemplateSchemaProperties(Schema):
    brand = fields.Str(required=True)
    style = fields.Str(required=True)
    genre = fields.Str(required=True)

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)


class ShoeTemplateSchema(ModelSchema):

    class Meta:
        model = "Model.Product.Template"

    properties = Nested(ShoeTemplateSchemaProperties(partial=True))


@register(Model.Product.Family, tablename=Model.Product.Family)
class ShoeFamilyTest(Model.Product.Family):
    FAMILY_CODE = "SHOES"
    family_schema = ShoeFamilySchema
    template_schema = ShoeTemplateSchema


@Declarations.register(Model.Product)
class Family:

    @classmethod
    def get_family_codes(cls):
        res = super(Family, cls).get_family_codes()
        res.update(dict(SHOES='Shoes'))
        return res
