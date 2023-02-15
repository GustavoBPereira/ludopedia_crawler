from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='hello')
def home_view(request):
    return Response('hello <3')
