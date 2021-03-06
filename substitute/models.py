"""
Models file
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField


class Profile(models.Model):
    """
    Model corresponding to the user profile with FK to User
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        """
        Meta class
        """
        ordering = ['id']

    def __str__(self):
        """
        Method returning the string profile
        :return:
        """
        return "Profile de {0}".format(self.user.username)


class Category(models.Model):
    """
    Class for category of article
    """
    name = models.CharField(
        max_length=600,
        help_text=_("The category name from openfoodfact api.")
    )

    class Meta:
        """
        Meta class
        """
        ordering = ['id']

    def __str__(self):
        return "{0}".format(self.name)


class Store(models.Model):
    """
    Class for store
    """
    name = models.CharField(
        max_length=600,
        help_text=_("The store name from openfoodfact api.")
    )

    class Meta:
        """
        Meta class
        """
        ordering = ['id']


class Article(models.Model):
    """
    Class for article
    """
    NUTRIGRAD = [
        ('a', "a"),
        ('b', "b"),
        ('c', "c"),
        ('d', "d"),
        ('e', "e"),
    ]

    stores = models.ManyToManyField(
        Store,
        related_name='articles',
        help_text=_("the relation with store model")
    )
    code = models.CharField(
        max_length=100,
        help_text=_("The BarCode from openfoodfact api.")
    )
    nutrition_grades = models.CharField(
        max_length=1,
        choices=NUTRIGRAD,
        help_text=_("The nutrition grade of article from openfoodfact api.")
    )
    id_api = models.CharField(
        max_length=600,
        help_text=_("The store id from openfoodfact api.")
    )
    categories = models.ManyToManyField(
        Category,
        related_name='articles',
        help_text=_("the relation with category model")
    )
    product_name = models.CharField(
        max_length=600,
        help_text=_("The article name from openfoodfact api.")
    )
    image_url = models.URLField(
        max_length=600,
        null=True,
        help_text=_("The url article image from openfoodfact api.")
    )
    nutriments = JSONField(
        default=list,
        null=True,
        help_text=_("List of article nutriments from openfoodfact api.")
    )
    url = models.URLField(
        max_length=600,
        null=True,
        help_text=_("The url article from openfoodfact api.")
    )
    ingredients = JSONField(
        default=list,
        null=True,
        help_text=_("List of article ingredients from openfoodfact api.")
    )
    keywords = JSONField(
        default=list,
        null=True,
        help_text=_("List of article _keywords from openfoodfact api.")
    )
    delete = models.CharField(
        max_length=20,
        null=True,
        help_text=_("Internal field for working.")
    )
    my_grade = models.PositiveIntegerField(
        null=True,
        help_text=_("Internal field for working.")
    )
    keywords_number = models.PositiveIntegerField(
        null=True,
        help_text=_("Internal field for working.")
    )
    ingredients_number = models.PositiveIntegerField(
        null=True,
        help_text=_("Internal field for working.")
    )

    class Meta:
        """
        Meta class
        """
        ordering = ['id']

    def get_article_substitutes_from_bd(self, category, nutriscore):
        """
        Method returning a list of articles could substitute the self searched_article from
        data_base
        :param category: search category
        :param nutriscore: search nutriscore
        :return: list of Article object
        """
        category = self.categories.all()[0] if not category else category
        substitutes = category.articles.all().filter(nutrition_grades=nutriscore) if \
            nutriscore else category.articles.all()
        substitutes = Article.filter_substitutes_by_keyword_and_ingredients(self, substitutes)

        return substitutes

    @staticmethod
    def filter_substitutes_by_keyword_and_ingredients(searched_article, substitutes):
        """
        Method filtering the substitutes by keyword and ingredients
        :param searched_article: searched_article object
        :param substitutes: list of substitutes (Articles objects)
        :return:
        """
        # delete article chosen by user for not include itself in search
        substitutes = [i for i in substitutes if i.code != searched_article.code]
        for substitute in substitutes:
            # count same keywords in field
            keywords_number = sum(1 for x in searched_article.keywords if x in substitute.keywords)
            substitute.keywords_number = keywords_number if keywords_number else 0

            # In order to sort the grade in the reverse order, I create my own reverse grade match
            grades_dict = {
                "a": 5,
                "b": 4,
                "c": 3,
                "d": 2,
                "e": 1,
                '': 0
            }

            substitute.my_grade = grades_dict[substitute.nutrition_grades] if grades_dict.get(
                substitute.nutrition_grades) else 0

            # count same ingredients
            # try is necessary because product are not always composed with text info and
            # rank info in ingredients field
            try:
                ingredients_number = sum(1 for x in
                                         [v.lower() for d in searched_article.ingredients for (k, v)
                                          in d.items() if k == "text"] if
                                         x in [v.lower() for d in substitute.ingredients for (k, v)
                                               in d.items() if k == "text"])
            except KeyError:
                ingredients_number = 0
            substitute.ingredients_number = ingredients_number

            if substitute.ingredients_number == 0 or substitute.keywords_number <= 3:
                substitute.delete = "delete"

        # impossible to delete an instance when the iterator works on it without breaking the loop
        # and skipping instances, it is why I write the delete key for copy in an other array,
        # only the necessary instances
        new_substitutes = []
        for substitute in substitutes:
            if not substitute.delete:
                new_substitutes.append(substitute)

        # sort the list of substitutes by ingredients_number, keywords_number, my_grade
        if new_substitutes:
            new_substitutes.sort(
                key=lambda x: [x.ingredients_number, x.keywords_number, x.my_grade], reverse=True)
            return new_substitutes
        return None

    @staticmethod
    def register_from_product(product):
        """
        Method registering article in data_base from product api
        :param product: product from api
        :return: article
        """
        code = product.get("code", None)
        nutrition_grades = product.get("nutrition_grades", None)
        id_api = product.get("id", None)
        product_name = product.get("product_name", "")
        nutriments = product.get("nutriments", {})
        image_url = product.get("image_url", None)
        url = product.get("url", None)
        ingredients = product.get("ingredients", None)
        keywords = product.get("_keywords", None)

        article = Article.objects.get_or_create(
            code=code,
            nutrition_grades=nutrition_grades,
            id_api=id_api,
            product_name=product_name,
            nutriments=nutriments,
            image_url=image_url,
            url=url,
            ingredients=ingredients,
            keywords=keywords
        )[0]

        stores = product.get("stores", None)
        if stores:
            for name in stores.split(','):
                article.stores.add(Store.objects.get_or_create(name=name)[0])
        article.save()

        return article

    @classmethod
    def filter_best_article(cls, results):
        """
        Method filtering the results by the mosted call category
        """
        best_cat = max(set([a.categories.all()[0].id for a in results]),
                       key=[a.categories.all()[0].id for a in results].count)
        results = results.filter(categories__id=best_cat)
        return results


class ProfileSubstitute(models.Model):
    """
    Class for substitute profile
    """
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='substitutes',
        help_text=_("the relation with Profile model")
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='substitutes',
        help_text=_("the relation with Article model")
    )
