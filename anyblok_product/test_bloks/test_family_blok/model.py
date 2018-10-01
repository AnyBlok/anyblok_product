from marshmallow import Schema, fields, validates_schema, ValidationError

from anyblok import Declarations

from anyblok_marshmallow import SchemaWrapper
from anyblok_marshmallow.fields import Nested, JsonCollection


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


class ShoeFamilySchema(SchemaWrapper):
    model = "Model.Product.Family"

    class Schema:
        properties = Nested(ShoeFamilySchemaProperties(partial=True))


class ShoeTemplateSchemaProperties(Schema):
    brand = JsonCollection(
                fieldname="properties",
                keys=['brands'],
                required=True)
    style = JsonCollection(
                fieldname="properties",
                keys=['styles'],
                required=True)
    genre = JsonCollection(
                fieldname="properties",
                keys=['genres'],
                required=True)

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)


class ShoeTemplateSchema(SchemaWrapper):
    model = "Model.Product.Template"

    class Schema:
        properties = Nested(ShoeTemplateSchemaProperties(partial=True))


class ShoeItemSchemaProperties(Schema):
    size = JsonCollection(
                fieldname="properties",
                keys=['sizes'],
                required=True)
    color = JsonCollection(
                fieldname="properties",
                keys=['colors'],
                required=True)

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)


class ShoeItemSchema(SchemaWrapper):
    model = "Model.Product.Item"

    class Schema:
        properties = Nested(ShoeItemSchemaProperties(partial=True))


@register(Model.Product.Family, tablename=Model.Product.Family)
class ShoeFamilyTest(Model.Product.Family):
    FAMILY_CODE = "SHOES"  # polymorphic identity
    family_schema = ShoeFamilySchema
    template_schema = ShoeTemplateSchema
    item_schema = ShoeItemSchema


@register(Model.Product)
class Family:

    @classmethod
    def get_family_codes(cls):
        res = super(Family, cls).get_family_codes()
        res.update(dict(SHOES='Shoes'))
        return res
