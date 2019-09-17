"""
Filter template
"""


from django import template
from substitute.models import ProfileSubstitute

register = template.Library()


@register.filter
def unregistred(article, user_id):
    """
    Filter to check if substitute always register for user
    :param article:
    :param user_id:
    :return:
    """
    substitute = ProfileSubstitute.objects.filter(profile__user__id=user_id, article__id=article.id)
    if substitute.count():
        return False
    return True

@register.filter
def get_item(dictionary, key):
    """
    Filter for getting item
    :param dictionary:
    :param key:
    :return:
    """
    return dictionary.get(key)
