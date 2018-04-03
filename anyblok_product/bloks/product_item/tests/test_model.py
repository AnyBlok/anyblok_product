from anyblok.tests.testcase import BlokTestCase


class TestProductModel(BlokTestCase):
    """ Test product model"""

    def setUp(self):
        super(TestProductModel, self).setUp()
        self.prod = self.registry.Product.Item.insert(
                sku="sku001",
                name="Foo",
                properties=dict(color="Blue", size="L"),
                description="Foo description")

    def test_product_creation_base(self):
        self.assertEqual(self.prod.sku, "sku001")

    def test_product_creation_properties(self):
        Item = self.registry.Product.Item

        self.assertIn("color", self.prod.properties.keys())
        self.assertNotIn("unexisting_property", self.prod.properties.keys())

        self.assertIn("Blue", self.prod.properties.values())
        self.assertNotIn("unexisting_value", self.prod.properties.values())

        self.assertEqual(self.prod.properties['color'], "Blue")
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
