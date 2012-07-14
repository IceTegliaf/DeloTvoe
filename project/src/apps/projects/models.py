# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Project(models.Model):
    name = models.CharField(_('name'), max_length=256)
    importance = models.PositiveSmallIntegerField(_('importance'), default=100)
    description = models.TextField(_('text'), blank=True)
    is_enable = models.BooleanField(_('is enabled'), default=True)
    
    class Meta:
        verbose_name=_('project')
        verbose_name_plural=_('projects')
        ordering=('importance',)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ("project_card", [self.id])