"""
Views
"""

# from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """
    Index view
    :param request:
    :return: HttpResponse with message
    """
    message = "Salut tout le monde !"
    return HttpResponse(message)
