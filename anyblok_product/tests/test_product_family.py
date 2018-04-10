from anyblok.tests.testcase import DBTestCase


class TestFamilyBlok(DBTestCase):
    blok_entry_points = ('bloks', 'test_bloks')

    def test_shoe_family_create(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        brands = ["Adibash", "Nixe", "Readbook"]
        sizes = ["39", "40", "41", "42", "43"]
        colors = ["white", "black", "red", "green", "blue"]
        styles = ["Sneakers", "Sandals", "Boat shoes"]
        genres = ["Men", "Women", "Kids"]

        shoe_family = registry.Product.Family.ShoeFamilyTest.create(
                code="SHOES", name="Shoes", description="Shoes description",
                properties=dict(
                    brands=brands,
                    sizes=sizes,
                    colors=colors,
                    styles=styles,
                    genres=genres)
                )
        self.assertTrue(
                isinstance(
                    shoe_family,
                    registry.Product.Family.ShoeFamilyTest
                    )
                )
        self.assertEqual(len(registry.Product.Family.query().all()), 1)
        self.assertEqual(registry.Product.Family.query().first().code, "SHOES")

    def test_shoe_family_create_fail_schema_validation_base(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(Exception) as context:
            shoe_family = registry.Product.Family.ShoeFamilyTest.create(
                            name="Shoes", description="Shoes description")
            self.assertTrue(
                    isinstance(
                        shoe_family,
                        Exception
                        )
                    )

        self.assertTrue('code' in context.exception.messages.keys())
        self.assertFalse('unexistingkey' in context.exception.messages.keys())
        self.assertDictEqual(
                dict(code=['Missing data for required field.']),
                context.exception.messages)

    def test_shoe_family_create_fail_schema_validation_unexisting_field(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(Exception) as context:
            shoe_family = registry.Product.Family.ShoeFamilyTest.create(
                            code="SHOES",
                            name="Shoes",
                            description="Shoes description",
                            unexisting_field="plop"
                            )
            self.assertTrue(
                    isinstance(
                        shoe_family,
                        Exception
                        )
                    )
        self.assertTrue(
                'unexisting_field' in context.exception.messages.keys())

    def test_shoe_family_create_fail_schema_validation_properties(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(Exception) as context:
            shoe_family = registry.Product.Family.ShoeFamilyTest.create(
                    code="SHOES",
                    name="Shoes",
                    description="Shoes description",
                    properties=dict(unexisting_schema_key=[])
                    )
            self.assertTrue(
                    isinstance(
                        shoe_family,
                        Exception
                        )
                    )

        self.assertTrue('properties' in context.exception.messages.keys())
        self.assertDictEqual(
                dict(properties=dict(unexisting_schema_key=['Unknown field'])),
                context.exception.messages)
