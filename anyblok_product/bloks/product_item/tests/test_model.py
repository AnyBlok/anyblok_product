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
        Item = self.registry.Product.Item
        props = dict(color="Blue", size="L")
        prod = Item.insert(
                sku="sku001", name="Foo", properties=props,
                description="Foo description")

        self.assertIn("color", prod.properties.keys())
        self.assertNotIn("unexisting_property", prod.properties.keys())

        self.assertIn("Blue", prod.properties.values())
        self.assertNotIn("unexisting_value", prod.properties.values())

        self.assertEqual(prod.properties['color'], "Blue")
        self.assertEqual(
            Item.query().filter(
                Item.properties['color'].astext == 'Red'
            ).count(), 0)
        self.assertEqual(
            Item.query().filter(
                Item.properties['color'].astext == 'Blue'
            ).count(), 1)

        self.assertEqual(
            Item.query().filter(
                Item.properties['unexisting_property'].astext == 'Blue'
            ).count(), 0)
