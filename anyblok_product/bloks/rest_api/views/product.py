from cornice.resource import resource

from anyblok_pyramid_rest_api.validator import model_schema_validator
from anyblok_pyramid_rest_api.crud_resource import CrudResource
from anyblok_pyramid import current_blok


MODEL = 'Model.Product'


@resource(
    collection_path='products',
    path='products/{id}',
    validators=(model_schema_validator,),
    installed_blok=current_blok()
)
class ProductResource(CrudResource):
    model = MODEL
