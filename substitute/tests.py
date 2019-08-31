"""
Tests
"""
from django.test import TestCase
from unittest.mock import patch

# Page accueil
    # doit renvoyer un 200
    # saisie dans cherche barre menu : saisie du nom tronqué du premier article doit renvoyer une liste de substitut
    # saisie dans cherche dans page : saisie du nom tronqué du premier article doit renvoyer une liste de substitut
from django.urls import reverse

from nutella import settings
from substitute.models import Article, register_api_data_db


class SearchPageTestCase(TestCase):
    """
    Test for search page
    """
    def setUp(self):
        """
        settings for test
        :return:
        """
        pass

    def test_search_page(self):
        """
        Test for status code 200
        :return:
        """
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_search_page(self):
        """
        Test search input
        :return:
        """
        register_api_data_db(2, 20, 20)
        article = Article.objects.filter(id=21)[0]
        if article:
            print(article.product_name)
            response = self.client.post(reverse('search'), {
                'chercher': article.product_name
            })
