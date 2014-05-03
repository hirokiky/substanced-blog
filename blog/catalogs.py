from substanced.catalog import (
    catalog_factory,
    indexview,
    Allowed,
    Text,
)
from substanced.util import get_content_type

from blog.features import get_features


@catalog_factory('blogentry')
class BlogEntryCatologFactory(object):
    titleentry = Text()
    allowed = Allowed(
        permissions=('sdi.view', 'view'),
    )


class BlogEntryCatalogViews(object):
    def __init__(self, resource):
        self.resource = resource

    @indexview(catalog_name='blogentry')
    def titleentry(self, default):
        content_type = get_content_type(self.resource)
        if content_type == 'Blog Entry':
            return get_features(self.resource.title) + get_features(self.resource.entry)
        else:
            return default
