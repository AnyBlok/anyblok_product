import pytest
from marshmallow import ValidationError


class TestBlokInstall:

    @pytest.fixture(autouse=True)
    def transact(self, request, registry_family_blok):
        transaction = registry_family_blok.begin_nested()
        request.addfinalizer(transaction.rollback)
        return


class TestFamilyBlok:
    blok_entry_points = ('bloks', 'test_bloks')

    @pytest.fixture(autouse=True)
    def transact(self, request, registry_family_blok):
        transaction = registry_family_blok.begin_nested()
        request.addfinalizer(transaction.rollback)
        return

    def test_shoe_family_create(self, registry_family_blok, shoe_family_dict):
        registry = registry_family_blok

        shoe_family = registry.Product.Family.ShoeFamilyTest.create(
            code="SHOES", name="Shoes", description="Shoes description",
            properties=shoe_family_dict
            )

        assert isinstance(
                shoe_family,
                registry.Product.Family.ShoeFamilyTest
                )

        assert registry.Product.Family.ShoeFamilyTest.query().count() == 1
        assert registry.Product.Family.ShoeFamilyTest.query(
                ).first().code == "SHOES"

    def test_family_namespace_query(self,
                                    registry_family_blok,
                                    shoe_family_dict,
                                    ):
        registry = registry_family_blok

        registry.Product.Family.insert(code="other")

        assert registry.Product.Family.query().count() == 1

        registry.Product.Family.ShoeFamilyTest.create(
            code="SHOES", name="Shoes", description="Shoes description",
            properties=shoe_family_dict
            )

        assert registry.Product.Family.query().count() == 2
        assert registry.Product.Family.ShoeFamilyTest.query().count() == 1
        assert (registry.Product.Family.ShoeFamilyTest.
                query().first().code) == "SHOES"

    def test_shoe_fam_create_fail_schema_validation_base(self,
                                                         registry_family_blok
                                                         ):
        registry = registry_family_blok

        with pytest.raises(ValidationError) as ctx:
            registry.Product.Family.ShoeFamilyTest.create(
                name="Shoes", description="Shoes description")

        assert 'code' in ctx.value.messages.keys()
        assert dict(code=['Missing data for required field.']
                    ) == ctx.value.messages

    def test_shoe_fam_create_fail_schema_valid_bad_field(self,
                                                         registry_family_blok
                                                         ):
        registry = registry_family_blok

        with pytest.raises(ValidationError) as ctx:
            registry.Product.Family.ShoeFamilyTest.create(
                    code="SHOES",
                    name="Shoes",
                    description="Shoes description",
                    unexisting_field="plop"
                    )
        assert 'unexisting_field' in ctx.value.messages.keys()

    def test_shoe_fam_create_fail_schema_validation_props(self,
                                                          registry_family_blok
                                                          ):
        registry = registry_family_blok

        with pytest.raises(ValidationError) as ctx:
            registry.Product.Family.ShoeFamilyTest.create(
                    code="SHOES",
                    name="Shoes",
                    description="Shoes description",
                    properties=dict(unexisting_schema_key=[])
                    )

        assert 'properties' in ctx.value.messages.keys()
        assert dict(properties=dict(
                    unexisting_schema_key=['Unknown field.'])
                    ) == ctx.value.messages

    def test_shoe_family_update(self,
                                shoe_family,
                                ):

        shoe_family.update(properties={'brands': 'Crocs'})
        assert shoe_family.properties['brands'] == 'Crocs'
        assert str(shoe_family.properties) == "{'brands': 'Crocs'}"

    def test_shoe_family_amend_existing_keys(self,
                                             shoe_family,
                                             ):

        original_keys = shoe_family.properties.copy().keys()
        shoe_family.amend(code="BOOTS", name="Boots")
        assert set(shoe_family.properties.keys()) == set(original_keys)
        assert shoe_family.name == "Boots"
        assert shoe_family.code == "BOOTS"

    def test_shoe_family_amend_unexisting_keys(self,
                                               shoe_family,
                                               ):
        with pytest.raises(ValidationError) as ctx:
            shoe_family.amend(unexisting_key="unexist")

        assert 'code' in ctx.value.messages.keys()
        assert 'unexisting_key' in ctx.value.messages.keys()

    def test_shoe_family_amend_bad_value(self,
                                         shoe_family,
                                         ):
        with pytest.raises(ValidationError) as ctx:
            shoe_family.amend(code=123)

        assert 'code' in ctx.value.messages.keys()
        assert dict(code=['Not a valid string.']
                    ) == ctx.value.messages

    def test_shoe_family_amend_properties_existing_keys(self,
                                                        shoe_family,
                                                        ):
        original_keys = shoe_family.properties.copy().keys()
        shoe_family_keys = shoe_family.properties.keys()
        shoe_family.amend(code="BOOTS", name="Boots",
                          properties={'brands': ['Crocs', 'Nike'],
                                      'sizes': ['37', '38']})
        assert set(shoe_family_keys) == set(original_keys)

    def test_shoe_family_amend_properties_unexisting_keys(self,
                                                          shoe_family,
                                                          ):
        with pytest.raises(ValidationError) as ctx:
            shoe_family.amend(code="BOOTS", name="Boots",
                              properties={'brands': ['Crocs', 'Nike'],
                                          'sizes': ['37', '38'],
                                          'unexisting_schema_key': []})

        assert 'properties' in ctx.value.messages.keys()
        assert dict(properties=dict(unexisting_schema_key=['Unknown field.'])
                    ) == ctx.value.messages

    def test_shoe_family_amend_properties_bad_value(self,
                                                    shoe_family,
                                                    ):
        with pytest.raises(ValidationError) as ctx:
            shoe_family.amend(code="BOOTS", name="Boots",
                              properties={'brands': [23],
                                          'sizes': ['37', '38'],
                                          })

            assert 'properties' in ctx.value.messages.keys()
            assert dict(properties=dict(
                        brands=['Not a valid string.'])
                        ) == ctx.value.messages


class TestTemplateBlok:
    blok_entry_points = ('bloks', 'test_bloks')

    @pytest.fixture(autouse=True)
    def transact(self, request, registry_family_blok):
        transaction = registry_family_blok.begin_nested()
        request.addfinalizer(transaction.rollback)
        return

    def test_shoe_template_create(self,
                                  registry_family_blok,
                                  shoe_family,
                                  ):

        registry = registry_family_blok
        shoe_template = registry.Product.Template.create(
                shoe_family,
                code="GAZGAZ",
                name="Gaz Gaz",
                description="Gaz Gaz template description",
                properties=dict(
                    brand="Adibash",
                    style="Sneakers",
                    genre="Unisex")
                )
        assert isinstance(shoe_template, registry.Product.Template)
        assert isinstance(shoe_template.family,
                          registry.Product.Family.ShoeFamilyTest
                          )
        assert registry.Product.Template.query().count() == 1
        assert registry.Product.Template.query().first().code == "GAZGAZ"

    def test_shoe_template_create_fail_schema_valid_base(self,
                                                         registry_family_blok,
                                                         shoe_family,
                                                         ):
        registry = registry_family_blok
        with pytest.raises(ValidationError) as ctx:
            registry.Product.Template.create(
                shoe_family,
                name="Gaz Gaz",
                description="Gaz Gaz template description",
                properties=dict(
                    brand="Adibash",
                    style="Sneakers",
                    genre="Unisex")
                )
            assert 'code' in ctx.value.messages.keys()

    def test_shoe_template_create_fail_schema_bad_field(self,
                                                        registry_family_blok,
                                                        shoe_family,
                                                        ):
        registry = registry_family_blok

        with pytest.raises(ValidationError) as ctx:
            registry.Product.Template.create(
                shoe_family,
                code="GAZGAZ",
                name="Gaz Gaz",
                description="Gaz Gaz template description",
                unexisting_field="plop",
                properties=dict(
                    brand="Adibash",
                    style="Sneakers",
                    genre="Unisex")
                )
            assert 'unexisting_field' in ctx.value.messages.keys()

    def test_shoe_template_create_fail_sch_props_bad_key(self,
                                                         registry_family_blok,
                                                         shoe_family,
                                                         ):
        registry = registry_family_blok

        with pytest.raises(ValidationError) as ctx:
            registry.Product.Template.create(
                shoe_family,
                code="GAZGAZ",
                name="Gaz Gaz",
                description="Gaz Gaz template description",
                properties=dict(
                    brand="Adibash",
                    style="Sneakers",
                    unexisting_key="plop",
                    genre="Unisex")
                )

            assert 'properties' in ctx.value.messages.keys()
            assert dict(properties=dict(unexisting_key=['Unknown field'])
                        ) == ctx.value.messages

    def test_shoe_template_create_fail_sch_props_bad_value(self,
                                                           shoe_family,
                                                           registry_family_blok
                                                           ):
        registry = registry_family_blok

        with pytest.raises(ValidationError) as ctx:
            registry.Product.Template.create(
                shoe_family,
                code="GAZGAZ",
                name="Gaz Gaz",
                description="Gaz Gaz template description",
                properties=dict(
                    brand="Adibash",
                    style="Sneakers",
                    genre="Bad value")
                )

            assert 'properties' in ctx.value.messages.keys()
            assert dict(properties=dict(genre=['Not a valid choice.'])
                        ) == ctx.value.messages

    def test_shoe_template_update(self,
                                  registry_family_blok,
                                  shoe_template,
                                  ):

        shoe_template.update(properties={'brand': 'Nike', 'style': 'Sandal'})
        assert shoe_template.properties['brand'] == 'Nike'
        assert shoe_template.properties['style'] == 'Sandal'
        assert len(shoe_template.properties) == len("{'brand': 'Nike',"
                                                 " 'style': 'Sandal'}")


class TestItemBlok:
    blok_entry_points = ('bloks', 'test_bloks')

    @pytest.fixture(autouse=True)
    def transact(self, request, registry_family_blok):
        transaction = registry_family_blok.begin_nested()
        request.addfinalizer(transaction.rollback)
        return

    def test_shoe_item_create(self, shoe_template, registry_family_blok):
        registry = registry_family_blok

        shoe_item = registry.Product.Item.create(
                shoe_template,
                code="GAZGAZ-BLUE-40",
                name="Gaz Gaz blue 40",
                description="Gaz Gaz blue 40 item description",
                properties=dict(
                    color="blue",
                    size="40")
                )

        assert isinstance(shoe_item, registry.Product.Item)
        assert isinstance(shoe_item.template.family,
                          registry.Product.Family.ShoeFamilyTest
                          )
        assert registry.Product.Item.query().count() == 1
        assert registry.Product.Item.query().first().code == "GAZGAZ-BLUE-40"

    def test_shoe_item_create_fail_schema_validation_base(self,
                                                          shoe_template,
                                                          registry_family_blok
                                                          ):
        registry = registry_family_blok

        with pytest.raises(ValidationError) as ctx:
            registry.Product.Item.create(
                    shoe_template,
                    name="Gaz Gaz blue 40",
                    description="Gaz Gaz blue 40 item description",
                    properties=dict(
                        color="blue",
                        size="40")
                    )
            assert 'code' in ctx.value.messages.keys()

    def test_shoe_item_create_fail_schema_valid_bad_field(self,
                                                          shoe_template,
                                                          registry_family_blok
                                                          ):
        registry = registry_family_blok

        with pytest.raises(ValidationError) as ctx:
            registry.Product.Item.create(
                    shoe_template,
                    code="GAZGAZ-BLUE-40",
                    name="Gaz Gaz blue 40",
                    unexisting_field="plop",
                    description="Gaz Gaz blue 40 item description",
                    properties=dict(
                        color="blue",
                        size="40")
                    )

            assert 'unexisting_field' in ctx.value.messages.keys()

    def test_shoe_item_create_fail_schema_props_bad_key(self,
                                                        shoe_template,
                                                        registry_family_blok,
                                                        ):
        registry = registry_family_blok

        with pytest.raises(ValidationError) as ctx:
            registry.Product.Item.create(
                    shoe_template,
                    code="GAZGAZ-BLUE-40",
                    name="Gaz Gaz blue 40",
                    description="Gaz Gaz blue 40 item description",
                    properties=dict(
                        color="blue",
                        unexisting_key="plop",
                        size="40")
                    )

            assert 'properties' in ctx.value.messages.keys()
            assert dict(properties=dict(unexisting_key=['Unknown field'])
                        ) == ctx.value.messages

    def test_shoe_item_create_fail_schema_props_bad_value(self,
                                                          shoe_template,
                                                          registry_family_blok,
                                                          ):
        registry = registry_family_blok

        with pytest.raises(ValidationError) as ctx:
            registry.Product.Item.create(
                    shoe_template,
                    code="GAZGAZ-BLUE-40",
                    name="Gaz Gaz blue 40",
                    description="Gaz Gaz blue 40 item description",
                    properties=dict(
                        color="blue",
                        unexisting_key="plop",
                        size="4000")
                    )

            assert 'properties' in ctx.value.messages.keys()
            assert dict(properties=dict(size=['Not a valid choice.'],
                        unexisting_key=['Unknown field.'])
                        ) == ctx.value.messages

    def test_shoe_item_create_collection(self,
                                         shoe_family,
                                         registry_family_blok
                                         ):
        registry = registry_family_blok

        Template = registry.Product.Template
        Item = registry.Product.Item

        for brand in shoe_family.properties['brands']:
            for style in shoe_family.properties['styles']:
                for genre in shoe_family.properties['genres']:
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
                    for color in shoe_family.properties['colors']:
                        for size in shoe_family.properties['sizes']:
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

        assert registry.Product.Template.query().count() == 36
        assert registry.Product.Item.query().count() == 900

        assert len(shoe_family.templates) == 36
        assert len(shoe_family.items) == 900

        assert Template.query().filter(
                Template.properties['brand'].has_key("Adibash") # noqa
            ).count() == 12

        assert Template.query().filter(
                Template.properties['brand'].has_key('Adibash')).filter( # noqa
                    Template.properties['genre'].has_key('Unisex') # noqa
            ).count() == 3

        assert Item.query().filter(
                Item.properties['color'].has_key('blue') # noqa
            ).count() == 180

        assert Item.query().filter(
                Item.properties['color'].has_key('blue')).filter( # noqa
                    Item.properties['size'].has_key('40') # noqa
            ).count() == 36
