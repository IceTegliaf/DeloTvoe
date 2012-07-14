# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.tools.shortcuts import get_settings
from apps.tools.text_parser import add_noindex_to_a
from pytils import translit



__all__ = ('Block', )

STATIC_BLOCKS_USE_CACHE = get_settings("STATIC_BLOCKS_USE_CACHE", True)
STATIC_BLOCKS_CACHE_KEY = get_settings("STATIC_BLOCKS_CACHE_KEY", "sb_%s_%s")
STATIC_BLOCKS_CACHE_TIMEOUT =  get_settings("STATIC_BLOCKS_CACHE_TIMEOUT", 86400) #1 day



# Create your models here.
class Block(models.Model):
    site = models.ForeignKey(Site, default=settings.SITE_ID)
    address = models.SlugField(_('address'),blank=True, db_index=True) # unique=True, - exclude for Language
    
    title = models.CharField(_('title'), blank=True, max_length=200)
    content = models.TextField(_('content'), blank=True)
    use_title = models.BooleanField(_('use title'), default=True)
    
    __unicode__ = lambda self: u'%s' % self.title
    
    def save(self, *args, **kwargs):
        
        if STATIC_BLOCKS_USE_CACHE:  
            cache.delete(STATIC_BLOCKS_CACHE_KEY % (self.address, self.site.id))
                      
        if self.address == '':
            self.address = translit.slugify(self.title)[:50]
        if not self.site: 
            self.site = Site.objects.get_current() 
        self.content = add_noindex_to_a(self.content)
        super(Block, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name        = _('Block')
        verbose_name_plural = _('Blocks')
        unique_together = [('site','address')]
        
        
    def save_to_cache(self):
        return {"title":self.title, "content": self.content,
                "use_title": self.use_title, "address":self.address,
                "id": self.id}


    def load_from_cache(self, data):
        self.title = data['title']
        self.content = data['content']
        self.use_title = data['use_title']
        self.address = data['address']
        self.id = data['id']
        