from anyblok.blok import Blok
from logging import getLogger
logger = getLogger(__name__)


class ProductFamilyBlok(Blok):
    """Product Family blok
    """
    version = "0.1.0"
    author = "Franck BRET"

    required = ['product_template']

    @classmethod
    def import_declaration_module(cls):
        from . import family # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import family
        reload(family)
