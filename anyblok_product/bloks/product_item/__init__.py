from anyblok.blok import Blok
from logging import getLogger
logger = getLogger(__name__)


class ProductItemBlok(Blok):
    """Product blok
    """
    version = "0.1.0"
    author = "Franck BRET"

    @classmethod
    def import_declaration_module(cls):
        from . import item # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import item
        reload(item)
