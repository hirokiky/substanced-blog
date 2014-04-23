import colander
import datetime
import time
import deform.widget

from persistent import Persistent
from pyramid.security import (
    Allow,
    Everyone,
)

from substanced.content import content
from substanced.folder import Folder
from substanced.property import PropertySheet
from substanced.schema import MultireferenceIdSchemaNode
from substanced.objectmap import (
    multireference_sourceid_property,
    multireference_source_property,
    multireference_targetid_property,
    multireference_target_property,
)
from substanced.root import Root
from substanced.schema import (
    Schema,
    NameSchemaNode,
)
from substanced.util import renamer, get_oid

from .interfaces import BlogEntryToTag


class TagSchema(Schema):
    name = NameSchemaNode(
        editing=lambda c, r: r.registry.content.istype(c, 'Tag')
    )


class TagPropertySheet(PropertySheet):
    schema = TagSchema()


@content(
    'Tag',
    add_view='add_tag',
    icon='glyphicon glyphicon-tag',
    propertysheets=(
        ('', TagPropertySheet),
    ),
    tab_order=('properties',),
)
class Tag(Persistent):
    name = renamer()
    entryids = multireference_targetid_property(BlogEntryToTag)
    entries = multireference_target_property(BlogEntryToTag)


@content(
    'Tags',
    icon='glyphicon glyphicon-tags',
)
class Tags(Folder):

    """ Folder for tags of a blog entry
    """

    def __sdi_addable__(self, context, introspectable):
        return introspectable.get('content_type') == 'Tag'


def tags_choices(context, request):
    blog = request.registry.content.find(context, 'Root')
    tags = blog.get('tags')
    values = [(get_oid(tag), name) for name, tag in tags.items()]
    return values


@colander.deferred
def now_default(node, kw):
    return datetime.datetime.now()


class BlogEntrySchema(Schema):
    name = NameSchemaNode(
        editing=lambda c, r: r.registry.content.istype(c, 'BlogEntry')
    )
    title = colander.SchemaNode(
        colander.String(),
    )
    entry = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget(rows=20, cols=70),
    )
    format = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['rst', 'html']),
        widget=deform.widget.SelectWidget(
            values=[('rst', 'rst'), ('html', 'html')]),
    )
    tagids = MultireferenceIdSchemaNode(
        choices_getter=tags_choices,
        title='Tags',
    )
    pubdate = colander.SchemaNode(
        colander.DateTime(default_tzinfo=None),
        default=now_default,
    )


class BlogEntryPropertySheet(PropertySheet):
    schema = BlogEntrySchema()


@content(
    'Blog Entry',
    icon='glyphicon glyphicon-book',
    add_view='add_blog_entry',
    propertysheets=(
        ('', BlogEntryPropertySheet),
    ),
    catalog=True,
    tab_order=('properties', 'contents', 'acl_edit'),
)
class BlogEntry(Folder):

    name = renamer()

    tagids = multireference_sourceid_property(BlogEntryToTag)
    tags = multireference_source_property(BlogEntryToTag)

    def __init__(self, title, entry, format, pubdate):
        Folder.__init__(self)
        self.title = title
        self.entry = entry
        self.format = format
        self.pubdate = pubdate
        self['attachments'] = Attachments()
        self['comments'] = Comments()

    def __sdi_addable__(self, context, introspectable):
        return False

    def add_comment(self, comment):
        while 1:
            name = str(time.time())
            if name not in self:
                self['comments'][name] = comment
                break


class CommentSchema(Schema):
    commenter = colander.SchemaNode(
        colander.String(),
    )
    text = colander.SchemaNode(
        colander.String(),
    )
    pubdate = colander.SchemaNode(
        colander.DateTime(),
        default=now_default,
    )


class CommentPropertySheet(PropertySheet):
    schema = CommentSchema()


@content(
    'Comment',
    icon='glyphicon glyphicon-comment',
    add_view='add_comment',
    propertysheets=(
        ('', CommentPropertySheet),
    ),
    catalog = True,
)
class Comment(Persistent):

    def __init__(self, commenter_name, text, pubdate):
        self.commenter_name = commenter_name
        self.text = text
        self.pubdate = pubdate


def comments_columns(folder, subobject, request, default_columnspec):
    pubdate = getattr(subobject, 'pubdate', None)
    if pubdate is not None:
        pubdate = pubdate.isoformat()

    return default_columnspec + [
        {'name': 'Publication date',
         'value': pubdate,
         'formatter': 'date',
         },
    ]


@content(
    'Comments',
    icon='glyphicon glyphicon-list',
    columns=comments_columns,
)
class Comments(Folder):

    """ Folder for comments of a blog entry
    """

    def __sdi_addable__(self, context, introspectable):
        return introspectable.get('content_type') == 'Comment'


def attachments_columns(folder, subobject, request, default_columnspec):
    kb_size = None
    if getattr(subobject, 'get_size', None) and callable(subobject.get_size):
        kb_size = int(int(subobject.get_size()) / 1000)

    return default_columnspec + [
        {'name': 'Size',
         'value': "%s kB" % kb_size,
         },
    ]


@content(
    'Attachments',
    icon='glyphicon glyphicon-list',
    columns=attachments_columns,
)
class Attachments(Folder):

    """ Folder for attachments of a blog entry
    """

    def __sdi_addable__(self, context, introspectable):
        return introspectable.get('content_type') == 'File'


class BlogSchema(Schema):

    """ The schema representing the blog root. """
    title = colander.SchemaNode(
        colander.String(),
        missing=''
    )
    description = colander.SchemaNode(
        colander.String(),
        missing=''
    )


class BlogPropertySheet(PropertySheet):
    schema = BlogSchema()


def blog_columns(folder, subobject, request, default_columnspec):
    title = getattr(subobject, 'title', None)
    pubdate = getattr(subobject, 'pubdate', None)
    if pubdate is not None:
        pubdate = pubdate.isoformat()

    return default_columnspec + [
        {'name': 'Title',
         'value': title,
         },
        {'name': 'Publication Date',
         'value': pubdate,
         'formatter': 'date',
         },
    ]


@content(
    'Root',
    icon='glyphicon glyphicon-home',
    propertysheets=(
        ('', BlogPropertySheet),
    ),
    after_create= ('after_create', 'after_create_blog'),
    columns=blog_columns,
)
class Blog(Root):
    title = 'Substance D Blog'
    description = 'Description of this blog'

    def __sdi_addable__(self, context, introspectable):
        return introspectable.get('content_type') == 'Blog Entry'

    @property
    def sdi_title(self):
        return self.title

    @sdi_title.setter
    def sdi_title(self, value):
        self.title = value

    def after_create_blog(self, inst, registry):
        acl = getattr(self, '__acl__', [])
        acl.append((Allow, Everyone, 'view'))
        self.__acl__ = acl

        # Adding a Tags folder
        tags = registry.content.create('Tags')
        tags.__sdi_deletable__ = False
        self.add('tags', tags, registry=registry)

        tag = registry.content.create('Tag')
        tags['testtag'] = tag
