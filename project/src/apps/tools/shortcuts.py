from django.shortcuts import render_to_response, _get_queryset
from django.template import RequestContext
from django.conf import settings
from apps.tools.json_rpc import to_json


def get_object_or_none(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
        

def get_settings(name, default=None):
    if hasattr(settings,name):
        return getattr(settings,name)
    return default


class Paginated(object):
    """Shit less, reusable and serializable paginator"""
    json_fields = (
        ('content', 'content_json'), 'page',
        'count', 'next_page_available',
        'prev_page_available',
    )

    def __init__(self, qs, page=0, per_page=getattr(settings, 'PER_PAGE', 10)):
        self.qs = qs
        self.page = int(page)
        self.per_page = int(per_page)

    @property
    def content(self):
        if not hasattr(self, '_content'):
            self._content = self.qs[self.page * self.per_page:][:self.per_page]
        return self._content

    @property
    def count(self):
        if not hasattr(self, '_count'):
            self._count = self.qs.count()
        return self._count

    def next_page_available(self):
        return self.count > (self.page + 1) * self.per_page

    def next_page(self):
        return self.page + 1

    def prev_page_available(self):
        return self.page > 0

    def prev_page(self):
        return self.page - 1

    def content_json(self):
        return map(to_json, self.content)

    def __iter__(self):
        for item in self.content:
            yield item


def paginate(qs, page, per_page=getattr(settings, 'PER_PAGE', 10)):  # Deprected
    page = int(page)
    return qs[page * per_page:][:per_page]
