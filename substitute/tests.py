"""
Tests
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from substitute.models import Article, register_api_data_db, valid_product, Profile, ProfileSubstitute


class SearchingPageTestCase(TestCase):
    """
    Test for search page
    """
    def test_register_api_data_db(self):
        """
        Test for register_api_data_db
        :return:
        """
        register_api_data_db(2, 20, 20)
        self.assertGreater(Article.objects.count(), 1)

    def test_valid_product(self):
        """
        Test for valid_product
        :return:
        """
        valid_product1 = {
            "categories": 'Desayunos,Untables,',
            "nutrition_grades": 'd',
            "code": '8437007759600',
            "id": '8437007759600',
            "_keywords": ['naturgreen', 'para'],
            "ingredients": [{'id': 'fr:CREMAAL AVELLANAS INGREDIENTES', 'rank': 1,
                             'text': 'CREMAAL AVELLANAS INGREDIENTES'}],
            "product_name_fr": "nutella",
        }
        valid_product2 = {
            "categories": 'Desayunos,Untables,',
            "nutrition_grades": 'd',
            "code": '8437007759600',
            "id": '8437007759600',
            "_keywords": ['naturgreen', 'para'],
            "ingredients": [{'id': 'fr:CREMAAL AVELLANAS INGREDIENTES', 'rank': 1,
                             'text': 'CREMAAL AVELLANAS INGREDIENTES'}],
            "product_name_fr": "",
            "product_name": "nutella",
        }
        response = valid_product(valid_product1)
        self.assertTrue(response)
        response = valid_product(valid_product2)
        self.assertTrue(response)

        for key in valid_product1.keys():
            invalid_1 = valid_product1.copy()
            del invalid_1[key]
            response = valid_product(invalid_1)
            self.assertFalse(response)

    def test_searching_page(self):
        """
        Test search input
        :return:
        """
        register_api_data_db(2, 20, 20)
        article = Article.objects.first()
        if article:
            # search existing article
            response = self.client.post(reverse('search'), {
                'searching': article.product_name
            })
            self.assertEqual(response.status_code, 200)

        # search not existing article
        response = self.client.post(reverse('search'), {
            'searching': "la tête à toto"
        })
        self.assertEqual(response.status_code, 200)

    def test_register_substitute_and_consult(self):
        """
        Test register substitute and consult
        :return:
        """
        register_api_data_db(2, 20, 20)
        article = Article.objects.first()

        username = "username"
        email = "email@email.com"
        password = "password"
        user = User.objects.create_user(username, email, password)
        Profile.objects.create(user=user)
        data = {
            'csrfmiddlewaretoken': ['kml1mLBvkNpg8j5uWFEqlh23v3ciBM8OStaxnJZe6QV9gsFeTLS7gOZ8g4XWraAQ'],
            'username': username,
            'password': password,
        }
        self.client.post(reverse('log_in'), data)
        count = ProfileSubstitute.objects.count()

        data = {
            "user_id": user.id,
            "searching": article.product_name,
            "article_id": article.id
        }

        response = self.client.post(reverse('results'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProfileSubstitute.objects.count(), count + 1)

        response = self.client.post(reverse('mysubstitutes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].dicts[3]['content_title'], 'Voici la liste de vos substitus :')

    def test_detail(self):
        """
        Test detail input
        :return:
        """
        register_api_data_db(2, 20, 20)
        article = Article.objects.filter(id=1)[0]
        if article:
            # search existing article
            response = self.client.post(reverse('detail', args=[article.id]))
            self.assertEqual(response.status_code, 200)

        # search not existing article
        response = self.client.post(reverse('detail', args=[9956]))
        self.assertEqual(response.status_code, 404)

    def test_register(self):
        """
        Test register input
        :return:
        """
        username = "username"
        email = "email@email.com"
        password = "password"
        data = {'csrfmiddlewaretoken': ['kml1mLBvkNpg8j5uWFEqlh23v3ciBM8OStaxnJZe6QV9gsFeTLS7gOZ8g4XWraAQ'],
                'username': username,
                'email': email,
                'password': password,
                'redirect_to': ['/']}

        count = Profile.objects.count()

        self.client.post(reverse('register'), data)
        profile = Profile.objects.first()

        self.assertEqual(Profile.objects.count(), count + 1)
        self.assertEqual(profile.user.username, username)
        self.assertEqual(profile.user.email, email)

    def test_login_logout_account(self):
        """
        Test login input and logout and account
        :return:
        """
        username = "username"
        email = "email@email.com"
        password = "password"
        user = User.objects.create_user(username, email, password)
        Profile.objects.create(user=user)
        data = {
            'csrfmiddlewaretoken': ['kml1mLBvkNpg8j5uWFEqlh23v3ciBM8OStaxnJZe6QV9gsFeTLS7gOZ8g4XWraAQ'],
            'username': username,
            'password': password,
        }

        self.client.post(reverse('log_in'), data)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.id)
        response = self.client.post(reverse('account'))
        self.assertEqual(response.status_code, 200)

        self.client.post(reverse('logout'))
        self.assertIsNone(self.client.session.get('_auth_user_id'))
        response = self.client.post(reverse('account'))
        self.assertEqual(response.status_code, 302)
