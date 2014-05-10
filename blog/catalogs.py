from substanced.catalog import (
    catalog_factory,
    indexview,
    indexview_defaults,
    Allowed,
    Text,
    Field,
)
from substanced.event import subscribe_created
from substanced.root import Root

from blog import resources as blog_resources
from blog.features import get_features


@subscribe_created(Root)
def created(event):
    root = event.object
    service = root['catalogs']
    service.add_catalog('blogentry', update_indexes=True)


@catalog_factory('blogentry')
class BlogEntryCatologFactory(object):
    titleentry = Text()
    pubdate = Field()
    allowed = Allowed(
        permissions=('sdi.view', 'view'),
    )


@indexview_defaults(catalog_name='blogentry')
class BlogEntryCatalogViews(object):
    def __init__(self, resource):
        self.resource = resource

    @indexview(context=blog_resources.BlogEntry)
    def titleentry(self, default):
        return get_features(self.resource.title) + get_features(self.resource.entry)

    @indexview(context=blog_resources.BlogEntry)
    @indexview(context=blog_resources.Comment)
    def pubdate(self, default):
        return getattr(self.resource, 'pubdate', default)
