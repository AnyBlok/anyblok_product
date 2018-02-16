from anyblok.blok import Blok
from logging import getLogger


logger = getLogger(__name__)


class ProductRestApiBlok(Blok):
    """Product rest api blok
    """
    version = "0.1.0"
    author = "Franck BRET"
    required = ['anyblok-core', 'product']

    def load(self):
        import anyblok_pyramid_rest_api  # noqa

    @classmethod
    def pyramid_load_config(cls, config):
        """Pyramid http server configuration / initialization
        """
        try:
            import anyblok_pyramid_rest_api  # noqa
        except ImportError:
            logger.warning("You need to install 'anyblok_pyramid_rest api' to"
                           "use product_rest_api views")

        # Scan available views
        config.scan(cls.__module__ + '.views')
