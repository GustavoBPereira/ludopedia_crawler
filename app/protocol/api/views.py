from pyramid.view import view_config

from infra.storage import filter_product_name_contains, filter_product_name_equals


@view_config(route_name='search', renderer='json')
def search_view(request):
    q = request.params.get('q', None)
    return filter_product_name_contains(q)


@view_config(route_name='detail', renderer='json')
def detail_view(request):
    q = request.params.get('q', None)
    return filter_product_name_equals(q)
