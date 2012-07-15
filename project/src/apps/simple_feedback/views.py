from apps.simple_feedback.forms import FeedbackForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
from django.conf import settings
from apps.tools.shortcuts import get_settings
from django.template.loader import render_to_string
from apps.tools.mail import send_mail
from django.utils.translation import ugettext
from apps.tools.decorators import render_to

FEEDBACK_EMAILS = get_settings("FEEDBACK_EMAILS", [])


@render_to
def form(req):
    out={}
    form_kwargs = {'initial': dict(map(lambda key: (key, force_unicode(req.GET[key])), req.GET))}
    if req.POST:
        out['form'] = form = FeedbackForm(req.POST, **form_kwargs)
        if form.is_valid():
            feedback = form.save()
            
            if FEEDBACK_EMAILS:
                
                send_mail(
                    ugettext('%(project_name)s: feedback') % {"project_name": settings.SITE_NAME},
                    render_to_string("simple_feedback/email.html", {
                        'site_name': settings.SITE_NAME,
                        'feedback':feedback, 
                        'url': '%s/admin/simple_feedback/feedback/%s/' % (settings.SITE_URL, feedback.id),
                    }),
                    feedback.email if feedback.email else settings.DEFAULT_FROM,
                    FEEDBACK_EMAILS,
                    content_subtype='html'
                )
            return HttpResponseRedirect(reverse("feedback_ok"))
        
    else:
        out['form'] = FeedbackForm(**form_kwargs)
    return out


@render_to
def ok(req):
    out={}
    return out
