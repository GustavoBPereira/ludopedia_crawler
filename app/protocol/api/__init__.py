def includeme(config):
    config.add_route('search', 'search')
    config.add_route('detail', 'detail')
    config.scan("app.protocol.api.views")
