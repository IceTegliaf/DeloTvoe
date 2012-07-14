from apps.staticpages.models import Page

def cp_pages(req):
    pages = Page.objects.all()
    return {
                'cp_pages': pages,
            }