from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods

from . import models
from . import serializers

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Imports for Generation Random String
from string import ascii_letters, digits
from random import choice


# Create your views here.


def generate_random_string(string_length=6):
    # Generates a random string
    random_string = ''
    alpha_numerals = ascii_letters + digits
    for _ in range(string_length):
        random_string = random_string + choice(alpha_numerals)
    return random_string


def shorten_url(url, domain):
    # Gets a random string and validates it against the database
    random_string = generate_random_string()
    service, created = models.UrlModel.objects.get_or_create(
        slug=random_string)
    if created:
        service.url = url
        short_url = f'https://{domain}/{random_string}/'
        service.short_url = short_url
        service.save()
        return service
    else:
        shorten_url(url, domain)


@api_view(['POST'])
def url_shortener_api(request):
    try:
        # The URL entered by the User
        users_url = request.data['url']

        # Gets the shortened record and serialize it
        domain = "tiny.ngoayuda.org"
        service = shorten_url(users_url, domain)
        service_serializer = serializers.ServiceSerializer(service, many=False)
        return Response(data={'success': True, 'data': service_serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(data={'success': False, 'message': f'{str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def redirect(request, slug):
    # Redirect short URL to its original URL, if it's valid
    try:
        service = models.UrlModel.objects.get(slug=slug)
        url = service.url
        return Response(data={'url': url}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response('/', status=status.HTTP_404_NOT_FOUND)
