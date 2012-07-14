from django import forms
from apps.simple_feedback.models import Feedback
#from captcha.fields import ReCaptchaField
from django.utils.translation import ugettext_lazy as _



class FeedbackForm(forms.ModelForm):
    #captcha = ReCaptchaField(label=_('captcha'))    
    
    class Meta:
        model = Feedback
        exclude = ("is_processed",)