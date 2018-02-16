from anyblok.blok import Blok
from logging import getLogger
logger = getLogger(__name__)


class ProductTemplateBlok(Blok):
    """ProductTemplate blok
    """
    version = "0.1.0"
    author = "Franck BRET"

    required = ['product_item']

    @classmethod
    def import_declaration_module(cls):
        from . import template # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import template
        reload(template)
