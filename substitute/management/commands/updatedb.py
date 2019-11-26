import os

import openfoodfacts
from django.core.management.base import BaseCommand

from substitute import utils
from substitute.models import Article, Category


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutella.settings.production')


class Command(BaseCommand):
    help = 'Command to update database with openfoodfacts api data'

    def handle(self, *args, **options):
        register_api_data_db(2, 5, 2)
        self.stdout.write('This was extremely simple!!!')


def register_api_data_db(categories_nb=20, product_number_by_category=200, max_page_by_category=200):
    """
    Method getting initial data from openfoodfacts api and storing them in database
    :return:
    """
    # get all categories from openfoodfacts api
    categories = utils.facets.get_categories()

    for category in categories[:categories_nb]:
        name = category.get('name', None)
        if name:
            category = Category.objects.get_or_create(name=name)[0]
            # some articles are not available, so count to force min 60 product available by category
            # but break after 14 pages
            page, count_product = 1, 0
            while page < max_page_by_category:
                products = openfoodfacts.products.get_by_category(name, page=page)
                for product in products:
                    if valid_product(product):
                        article = Article.register_from_product(product)
                        article.categories.add(category)
                        count_product = (count_product + 1) if article else count_product
                    if count_product >= product_number_by_category:
                        break
                page += 1
                if count_product >= product_number_by_category:
                    break


def valid_product(product):
    """
    Method verifying existing field : minimum
    :param product: product dict from api
    :return: Boolean
    """
    # check if article already existing
    id_api = product.get("id", None)
    if not id_api or Article.objects.filter(id_api=id_api).exists():
        return False

    # check if minimum keys exist in product
    keys = [
        "nutrition_grades",
        "categories",
        "code",
        "id",
        "_keywords",
        "ingredients"
    ]
    for key in keys:
        if not product.get(key) or product.get(key) == ['']:
            return False
    if not product.get("product_name_fr") or product.get('product_name_fr') == ['']:
        if not product.get("product_name") or product.get('product_name') == ['']:
            return False

    return True