from anyblok.conftest import * # noqa
from anyblok.tests.conftest import * # noqa
import pytest


_BRANDS = ["Adibash", "Nixe", "Readbook"]
_SIZES = ["39", "40", "41", "42", "43"]
_COLORS = ["white", "black", "red", "green", "blue"]
_STYLES = ["Sneakers", "Sandals", "Boat shoes"]
_GENRES = ["Men", "Women", "Kids", "Unisex"]


@pytest.fixture(scope="class")
def registry_family_blok(testbloks_loaded):
    # flake8 was being capricious here about import, so I added a noqa
    registry = init_registry_with_bloks(['test_family_blok'], None) # noqa
    return registry


@pytest.fixture
def shoe_family(registry_family_blok):
    registry = registry_family_blok
    return registry.Product.Family.ShoeFamilyTest.create(
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


@pytest.fixture
def shoe_family_dict():
    return dict(
                brands=_BRANDS,
                sizes=_SIZES,
                colors=_COLORS,
                styles=_STYLES,
                genres=_GENRES
                )


@pytest.fixture
def shoe_template(registry_family_blok, shoe_family):
    registry = registry_family_blok
    return registry.Product.Template.create(
            shoe_family,
            code="GAZGAZ",
            name="Gaz Gaz",
            description="Gaz Gaz template description",
            properties=dict(
                brand="Adibash",
                style="Sneakers",
                genre="Unisex")
            )


@pytest.fixture
def shoe_item(registry_family_blok, shoe_family):
    registry = registry_family_blok
    return registry.Product.Item.create(
            shoe_template,
            code="GAZGAZ-BLUE-40",
            name="Gaz Gaz blue 40",
            description="Gaz Gaz blue 40 item description",
            properties=dict(
                color="blue",
                size="40")
            )
