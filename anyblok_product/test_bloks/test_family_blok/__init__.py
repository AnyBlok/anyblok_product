from anyblok.blok import Blok


class TestFamilyBlok(Blok):
    """Add attachment in AnyBlok"""

    version = '1.0.0'
    required = ['product_family']

    author = 'Franck Bret'

    @classmethod
    def import_declaration_module(cls):
        from . import model  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import model
        reload(model)
