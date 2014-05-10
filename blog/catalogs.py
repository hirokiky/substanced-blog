from substanced.catalog import (
    catalog_factory,
    indexview,
    indexview_defaults,
    Allowed,
    Text,
)

from blog import resources as blog_resources
from blog.features import get_features


@catalog_factory('blogentry')
class BlogEntryCatologFactory(object):
    titleentry = Text()
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
