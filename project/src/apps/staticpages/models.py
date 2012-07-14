# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pytils import translit
#from apps.staticpages.ping import ping
from django.template.loader         import render_to_string


__all__ = ('Page', )


# Create your models here.
class Page(models.Model):
    title = models.CharField(_('title'), max_length=200)
    show_title = models.BooleanField(_("show title"), default=True)
    address = models.SlugField(_('address'),blank=True) # unique=True, - exclude for Language
#    announce = models.TextField(_('announce'), blank=True)
    content = models.TextField(_('content'), blank=True)
    published = models.BooleanField(_('published'), default=True)
    
    
    #Метатэги
    seo_title       = models.CharField(_('title for SEO'), max_length=255, blank=True)
    seo_keywords    = models.CharField(_('keywords for SEO'), max_length=255, blank=True)
    seo_description = models.CharField(_('description for SEO'), max_length=255, blank=True)
    
    __unicode__ = lambda self: u'%s' % self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('staticpages_page', [self.address])
    
    def save(self, *args, **kwargs):
        if self.address == '':
            self.address = translit.slugify(self.title)[:50]
        
#        self.content = add_noindex_to_a(self.content)
        super(Page, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name        = _('page')
        verbose_name_plural = _('pages')

