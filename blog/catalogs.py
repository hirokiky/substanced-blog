from substanced.catalog import (
    catalog_factory,
    indexview,
    Allowed,
    Text,
)
from substanced.util import get_content_type


@catalog_factory('blogentry')
class BlogEntryCatologFactory(object):
    entry = Text()
    allowed = Allowed(
        permissions=('sdi.view', 'view'),
    )


class BlogEntryCatalogViews(object):
    def __init__(self, resource):
        self.resource = resource

    @indexview(catalog_name='blogentry')
    def entry(self, default):
        content_type = get_content_type(self.resource)
        if content_type == 'Blog Entry':
            return self.resource.entry
        else:
            return default
