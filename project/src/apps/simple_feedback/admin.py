# coding: utf-8
__author__ = "Kovalenko Pavel <pavel@bitrain.ru>"
__date__ = "$Date: 2011-09-15 13:00:23 +0400 (Чт, 15 сен 2011) $"
__version__ = "$Rev: 7036 $"

from apps.simple_feedback.models import Feedback
from django.contrib import admin


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('fio','email','phone','is_processed','create')
    list_filter = ('is_processed',)
    search_fields = ("fio", 'message')
    list_editable = ('is_processed', )
    date_hierarchy = 'create'
admin.site.register(Feedback, FeedbackAdmin)