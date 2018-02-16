from anyblok.tests.testcase import BlokTestCase


class TestProductModel(BlokTestCase):
    """ Test product model"""

    def test_product_creation_base(self):
        prod = self.registry.Product.Item.insert(
                sku="sku001",
                name="Foo",
                description="Foo description")

        self.assertEqual(prod.sku, "sku001")

    def test_product_creation_properties(self):
        props = dict(color="Blue", size="L")
        prod = self.registry.Product.Item.insert(sku="sku001", name="Foo",
                                                 properties=props,
                                                 description="Foo description")
        self.assertEqual(prod.properties['color'], "Blue")
        self.assertIn("color", prod.properties.keys())
        self.assertIn("Blue", prod.properties.values())
