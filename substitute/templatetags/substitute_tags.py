from django import template

from substitute.models import ProfileSubstitute

register = template.Library()


@register.filter
def unregistred(article, user_id):
    substitute = ProfileSubstitute.objects.filter(profile__user__id=user_id, article__id=article.id)
    if substitute.count():
        return False
    return True

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
