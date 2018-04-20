from anyblok.blok import Blok


class TestFamilyBlok(Blok):
    """Test Family Blok"""

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
