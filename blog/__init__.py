from pyramid.config import Configurator

from substanced import root_factory
from substanced.event import subscribe_created
from substanced.root import Root


def main(global_config, **settings):
    config = Configurator(settings=settings, root_factory=root_factory)
    config.include('substanced')
    config.add_static_view('static', 'static', cache_max_age=86400)
    config.add_static_view('bootstrap', 'bootstrap', cache_max_age=86400)
    config.scan()
    return config.make_wsgi_app()


@subscribe_created(Root)
def created(event):
    root = event.object
    service = root['catalogs']
    service.add_catalog('blogentry', update_indexes=True)
