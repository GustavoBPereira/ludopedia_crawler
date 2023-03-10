from pyramid.response import Response
from pyramid.view import view_config

from infra.storage import filter_product_name_contains, filter_product_name_equals

DEFAULT_RESPONSE_HEADERS = {'Access-Control-Allow-Origin': '*'}


@view_config(route_name='search', renderer='json')
def search_view(request):
    q = request.params.get('q', None)
    return Response(
        content_type='application/json',
        headers=DEFAULT_RESPONSE_HEADERS,
        json_body=filter_product_name_contains(q)
    )


@view_config(route_name='detail', renderer='json')
def detail_view(request):
    q = request.params.get('q', None)
    not_sold = True if request.params.get('include_not_sold', 'false') == 'true' else False
    return Response(
        content_type='application/json',
        headers=DEFAULT_RESPONSE_HEADERS,
        json_body=filter_product_name_equals(q, not_sold)
    )
