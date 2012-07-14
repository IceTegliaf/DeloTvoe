# coding: utf-8
__author__ = "Kovalenko Pavel <pavel@bitrain.ru>"
__date__ = "$Date: 2011-09-15 13:00:23 +0400 (Чт, 15 сен 2011) $"
__version__ = "$Rev: 7036 $"
#
from django.utils.translation import ugettext_lazy as _
from django.db import models
import datetime


class Feedback(models.Model):
    fio = models.CharField(max_length=255, verbose_name=_('FIO'))
    create = models.DateTimeField(_('created date'), auto_now_add = True, default=datetime.datetime.today)
    email = models.EmailField(verbose_name=_('email'))
    phone = models.CharField(max_length=255, verbose_name=_('phone'))
    message = models.TextField(verbose_name=_('message'))
    is_processed = models.BooleanField(_('is processed'), default=False)
    
    class Meta:
        verbose_name = _('feedback')
        verbose_name_plural = _('feedback')