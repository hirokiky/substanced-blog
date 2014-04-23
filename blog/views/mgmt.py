from webob.exc import HTTPFound
from substanced.sdi import mgmt_view
from substanced.form import FormView

from ..resources import PageSchema, TagSchema, BlogEntrySchema


@mgmt_view(
    content_type='Pages',
    name='add_page',
    permission='sdi.add-content',
    renderer='substanced.sdi:templates/form.pt',
    tab_condition=False,
)
class AddPageView(FormView):
    title = 'Add Page'
    schema = PageSchema()
    buttons = ('add',)

    def add_success(self, appstruct):
        name = appstruct.pop('name')
        request = self.request
        tag = request.registry.content.create('Page', **appstruct)
        self.context[name] = tag
        loc = request.mgmt_path(self.context, name, '@@properties')
        return HTTPFound(location=loc)


@mgmt_view(
    content_type='Tags',
    name='add_tag',
    permission='sdi.add-content',
    renderer='substanced.sdi:templates/form.pt',
    tab_condition=False,
)
class AddTagView(FormView):
    title = 'Add Tag'
    schema = TagSchema()
    buttons = ('add',)

    def add_success(self, appstruct):
        name = appstruct.pop('name')
        request = self.request
        tag = request.registry.content.create('Tag')
        self.context[name] = tag
        loc = request.mgmt_path(self.context, name, '@@properties')
        return HTTPFound(location=loc)


@mgmt_view(
    content_type='Root',
    name='add_blog_entry',
    permission='sdi.add-content',
    renderer='substanced.sdi:templates/form.pt',
    tab_condition=False,
)
class AddBlogEntryView(FormView):
    title = 'Add Blog Entry'
    schema = BlogEntrySchema()
    buttons = ('add',)

    def add_success(self, appstruct):
        name = appstruct.pop('name')
        request = self.request
        tagids = appstruct.pop('tagids')
        blogentry = request.registry.content.create('Blog Entry', **appstruct)
        self.context[name] = blogentry
        blogentry.tagids = tagids
        loc = request.mgmt_path(self.context, name, '@@properties')
        return HTTPFound(location=loc)
