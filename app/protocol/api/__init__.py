def includeme(config):
    config.add_route('hello', '')
    config.scan("app.protocol.api.views")
