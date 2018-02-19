#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for anyblok_product"""

from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'),
          'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(os.path.join(here, 'CHANGELOG.rst'),
          'r', encoding='utf-8') as changelog_file:
    changelog = changelog_file.read()

with open(os.path.join(here, 'VERSION'),
          'r', encoding='utf-8') as version_file:
    version = version_file.read().strip()

requirements = [
    'anyblok',
    'anyblok_postgres',
]

test_requirements = [
    # TODO: put package test requirements here
]

bloks = [
    'product_item=anyblok_product.bloks.product_item:ProductItemBlok',
    (
        'product_template=anyblok_product.bloks.product_template:'
        'ProductTemplateBlok'
    ),
    'product_family=anyblok_product.bloks.product_family:ProductFamilyBlok',
],

setup(
    name='anyblok_product',
    version=version,
    description="Anyblok blok for Product management.",
    long_description=readme + '\n\n' + changelog,
    author="Franck Bret",
    author_email='franckbret@gmail.com',
    url='https://github.com/franckbret/anyblok_product',
    packages=find_packages(),
    entry_points={
        'bloks': bloks,
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='anyblok, product, family, template, item',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
