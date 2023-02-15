from pyramid.config import Configurator


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""

    with Configurator(settings=settings) as config:
        config.include("app.infra")
        config.include("app.domain")
        config.include("app.protocol")
        return config.make_wsgi_app()
