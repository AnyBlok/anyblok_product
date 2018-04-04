from anyblok.tests.testcase import DBTestCase

class TestFamilyBlok(DBTestCase):
    blok_entry_points = ('bloks', 'test_bloks')

    def test_(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))
        sch = registry.Product.Family.ShoeFamilyTest.family_schema(registry=registry)
        shoe_family = registry.Product.Family.ShoeFamilyTest.create(code="SHOES", name="Shoes",
                description="Shoes description", properties="")
        shirt_family = registry.Product.Family.ShoeFamilyTest.create(name="Shirts")
