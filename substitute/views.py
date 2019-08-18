"""
Views
"""

# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    """
    Index view
    :param request:
    :return: HttpResponse with message
    """
    template = loader.get_template('substitute/index.html')
    return HttpResponse(template.render(request=request))
