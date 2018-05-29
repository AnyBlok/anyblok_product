from anyblok.tests.testcase import DBTestCase

from marshmallow.exceptions import ValidationError


_BRANDS = ["Adibash", "Nixe", "Readbook"]
_SIZES = ["39", "40", "41", "42", "43"]
_COLORS = ["white", "black", "red", "green", "blue"]
_STYLES = ["Sneakers", "Sandals", "Boat shoes"]
_GENRES = ["Men", "Women", "Kids", "Unisex"]


class TestFamilyBlok(DBTestCase):
    blok_entry_points = ('bloks', 'test_bloks')

    def test_shoe_family_create(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        shoe_family = registry.Product.Family.ShoeFamilyTest.create(
            code="SHOES", name="Shoes", description="Shoes description",
            properties=dict(
                brands=_BRANDS,
                sizes=_SIZES,
                colors=_COLORS,
                styles=_STYLES,
                genres=_GENRES)
            )
        self.assertTrue(
            isinstance(
                shoe_family,
                registry.Product.Family.ShoeFamilyTest
                )
            )
        self.assertEqual(
            registry.Product.Family.ShoeFamilyTest.query().count(),
            1
        )
        self.assertEqual(
            registry.Product.Family.ShoeFamilyTest.query().first().code,
            "SHOES")

    def test_family_namespace_query(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        registry.Product.Family.insert(code="other")

        self.assertEqual(registry.Product.Family.query().count(), 1)

        registry.Product.Family.ShoeFamilyTest.create(
            code="SHOES", name="Shoes", description="Shoes description",
            properties=dict(
                brands=_BRANDS,
                sizes=_SIZES,
                colors=_COLORS,
                styles=_STYLES,
                genres=_GENRES)
            )

        self.assertEqual(
            registry.Product.Family.query().count(),
            2
        )
        self.assertEqual(
            registry.Product.Family.ShoeFamilyTest.query().count(),
            1
        )
        self.assertEqual(
            registry.Product.Family.ShoeFamilyTest.query().first().code,
            "SHOES"
        )

    def test_shoe_family_create_fail_schema_validation_base(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(ValidationError) as ctx:
            registry.Product.Family.ShoeFamilyTest.create(
                name="Shoes", description="Shoes description")

            self.assertTrue('code' in ctx.exception.messages.keys())
            self.assertFalse('unexistingkey' in ctx.exception.messages.keys())
            self.assertDictEqual(
                    dict(code=['Missing data for required field.']),
                    ctx.exception.messages)

    def test_shoe_family_create_fail_schema_validation_unexisting_field(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(ValidationError) as ctx:
            registry.Product.Family.ShoeFamilyTest.create(
                    code="SHOES",
                    name="Shoes",
                    description="Shoes description",
                    unexisting_field="plop"
                    )
            self.assertTrue(
                    'unexisting_field' in ctx.exception.messages.keys())

    def test_shoe_family_create_fail_schema_validation_properties(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(ValidationError) as ctx:
            registry.Product.Family.ShoeFamilyTest.create(
                    code="SHOES",
                    name="Shoes",
                    description="Shoes description",
                    properties=dict(unexisting_schema_key=[])
                    )

            self.assertTrue('properties' in ctx.exception.messages.keys())
            self.assertDictEqual(
                    dict(
                        properties=dict(
                            unexisting_schema_key=['Unknown field'])),
                    ctx.exception.messages)


class TestTemplateBlok(DBTestCase):
    blok_entry_points = ('bloks', 'test_bloks')

    def create_shoe_family(self):
        return self.registry.Product.Family.ShoeFamilyTest.create(
                code="SHOES",
                name="Shoes",
                description="Shoes description",
                properties=dict(
                    brands=_BRANDS,
                    sizes=_SIZES,
                    colors=_COLORS,
                    styles=_STYLES,
                    genres=_GENRES)
                )

    def test_shoe_template_create(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        shoe_template = registry.Product.Template.create(
                self.create_shoe_family(),
                code="GAZGAZ",
                name="Gaz Gaz",
                description="Gaz Gaz template description",
                properties=dict(
                    brand="Adibash",
                    style="Sneakers",
                    genre="Unisex")
                )
        self.assertTrue(
                isinstance(
                    shoe_template,
                    registry.Product.Template
                    )
                )
        self.assertTrue(
                isinstance(
                    shoe_template.family,
                    registry.Product.Family.ShoeFamilyTest
                    )
                )
        self.assertEqual(registry.Product.Template.query().count(), 1)
        self.assertEqual(
                registry.Product.Template.query().first().code,
                "GAZGAZ"
                )

    def test_shoe_template_create_fail_schema_validation_base(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(ValidationError) as ctx:
            registry.Product.Template.create(
                self.create_shoe_family(),
                name="Gaz Gaz",
                description="Gaz Gaz template description",
                properties=dict(
                    brand="Adibash",
                    style="Sneakers",
                    genre="Unisex")
                )
            self.assertTrue('code' in ctx.exception.messages.keys())

    def test_shoe_template_create_fail_schema_validation_bad_field(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(ValidationError) as ctx:
            registry.Product.Template.create(
                self.create_shoe_family(),
                code="GAZGAZ",
                name="Gaz Gaz",
                description="Gaz Gaz template description",
                unexisting_field="plop",
                properties=dict(
                    brand="Adibash",
                    style="Sneakers",
                    genre="Unisex")
                )
            self.assertTrue(
                    'unexisting_field' in ctx.exception.messages.keys())

    def test_shoe_template_create_fail_schema_props_unexisting_json_key(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(ValidationError) as ctx:
            registry.Product.Template.create(
                self.create_shoe_family(),
                code="GAZGAZ",
                name="Gaz Gaz",
                description="Gaz Gaz template description",
                properties=dict(
                    brand="Adibash",
                    style="Sneakers",
                    unexisting_key="plop",
                    genre="Unisex")
                )

            self.assertTrue('properties' in ctx.exception.messages.keys())
            self.assertDictEqual(
                    dict(properties=dict(unexisting_key=['Unknown field'])),
                    ctx.exception.messages)

    def test_shoe_template_create_fail_schema_props_bad_value(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(ValidationError) as ctx:
            registry.Product.Template.create(
                self.create_shoe_family(),
                code="GAZGAZ",
                name="Gaz Gaz",
                description="Gaz Gaz template description",
                properties=dict(
                    brand="Adibash",
                    style="Sneakers",
                    genre="Bad value")
                )

        self.assertTrue('properties' in ctx.exception.messages.keys())
        self.assertDictEqual(
                dict(properties=dict(genre=['Not a valid choice.'])),
                ctx.exception.messages)


class TestItemBlok(DBTestCase):
    blok_entry_points = ('bloks', 'test_bloks')

    def create_shoe_template(self):
        shoe_family = self.registry.Product.Family.ShoeFamilyTest.create(
                code="SHOES",
                name="Shoes",
                description="Shoes description",
                properties=dict(
                    brands=_BRANDS,
                    sizes=_SIZES,
                    colors=_COLORS,
                    styles=_STYLES,
                    genres=_GENRES)
                )
        return self.registry.Product.Template.create(
                shoe_family,
                code="GAZGAZ",
                name="Gaz Gaz",
                description="Gaz Gaz template description",
                properties=dict(
                    brand="Adibash",
                    style="Sneakers",
                    genre="Unisex")
                )

    def test_shoe_item_create(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        shoe_item = registry.Product.Item.create(
                self.create_shoe_template(),
                code="GAZGAZ-BLUE-40",
                name="Gaz Gaz blue 40",
                description="Gaz Gaz blue 40 item description",
                properties=dict(
                    color="blue",
                    size="40")
                )

        self.assertTrue(
                isinstance(
                    shoe_item,
                    registry.Product.Item
                    )
                )
        self.assertTrue(
                isinstance(
                    shoe_item.template.family,
                    registry.Product.Family.ShoeFamilyTest
                    )
                )
        self.assertEqual(registry.Product.Item.query().count(), 1)
        self.assertEqual(
                registry.Product.Item.query().first().code,
                "GAZGAZ-BLUE-40"
                )

    def test_shoe_item_create_fail_schema_validation_base(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(ValidationError) as ctx:
            registry.Product.Item.create(
                    self.create_shoe_template(),
                    name="Gaz Gaz blue 40",
                    description="Gaz Gaz blue 40 item description",
                    properties=dict(
                        color="blue",
                        size="40")
                    )
            self.assertTrue('code' in ctx.exception.messages.keys())

    def test_shoe_item_create_fail_schema_validation_bad_field(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(ValidationError) as ctx:
            registry.Product.Item.create(
                    self.create_shoe_template(),
                    code="GAZGAZ-BLUE-40",
                    name="Gaz Gaz blue 40",
                    unexisting_field="plop",
                    description="Gaz Gaz blue 40 item description",
                    properties=dict(
                        color="blue",
                        size="40")
                    )

            self.assertTrue(
                    'unexisting_field' in ctx.exception.messages.keys())

    def test_shoe_item_create_fail_schema_props_unexisting_json_key(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(ValidationError) as ctx:
            registry.Product.Item.create(
                    self.create_shoe_template(),
                    code="GAZGAZ-BLUE-40",
                    name="Gaz Gaz blue 40",
                    description="Gaz Gaz blue 40 item description",
                    properties=dict(
                        color="blue",
                        unexisting_key="plop",
                        size="40")
                    )

            self.assertTrue('properties' in ctx.exception.messages.keys())
            self.assertDictEqual(
                    dict(properties=dict(unexisting_key=['Unknown field'])),
                    ctx.exception.messages)

    def test_shoe_item_create_fail_schema_props_bad_value(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        with self.assertRaises(ValidationError) as ctx:
            registry.Product.Item.create(
                    self.create_shoe_template(),
                    code="GAZGAZ-BLUE-40",
                    name="Gaz Gaz blue 40",
                    description="Gaz Gaz blue 40 item description",
                    properties=dict(
                        color="blue",
                        unexisting_key="plop",
                        size="4000")
                    )

        self.assertTrue('properties' in ctx.exception.messages.keys())
        self.assertDictEqual(
                dict(properties=dict(size=['Not a valid choice.'])),
                ctx.exception.messages)

    def test_shoe_item_create_collection(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_family_blok',))

        Template = self.registry.Product.Template
        Item = self.registry.Product.Item

        shoe_family = self.registry.Product.Family.ShoeFamilyTest.create(
                code="SHOES",
                name="Shoes",
                description="Shoes description",
                properties=dict(
                    brands=_BRANDS,
                    sizes=_SIZES,
                    colors=_COLORS,
                    styles=_STYLES,
                    genres=_GENRES)
                )
        for brand in _BRANDS:
            for style in _STYLES:
                for genre in _GENRES:
                    template = registry.Product.Template.create(
                        shoe_family,
                        code="%s-%s-%s" % (brand, style, genre),
                        name="%s %s %s" % (brand, style, genre),
                        description="Template %s %s %s" % (
                            brand, style, genre),
                        properties=dict(
                            brand=brand,
                            style=style,
                            genre=genre)
                        )
                    for color in _COLORS:
                        for size in _SIZES:
                            Item.create(
                                template,
                                code="%s-%s-%s-%s-%s" % (
                                    brand, style, genre, color, size),
                                name="%s %s %s %s %s" % (
                                    brand, style, genre, color, size),
                                description="Item %s %s %s %s %s" % (
                                    brand, style, genre, color, size),
                                properties=dict(
                                    color=color,
                                    size=size)
                                )

        self.assertEqual(registry.Product.Template.query().count(), 36)
        self.assertEqual(registry.Product.Item.query().count(), 900)

        self.assertEqual(len(shoe_family.templates), 36)
        self.assertEqual(len(shoe_family.items), 900)

        self.assertEqual(
            Template.query().filter(
                Template.properties['brand'].astext == 'Adibash'
            ).count(), 12)

        self.assertEqual(
            Template.query().filter(
                Template.properties['brand'].astext == 'Adibash').filter(
                    Template.properties['genre'].astext == 'Unisex'
            ).count(), 3)

        self.assertEqual(
            Item.query().filter(
                Item.properties['color'].astext == 'blue'
            ).count(), 180)

        self.assertEqual(
            Item.query().filter(
                Item.properties['color'].astext == 'blue').filter(
                    Item.properties['size'].astext == '40'
            ).count(), 36)
