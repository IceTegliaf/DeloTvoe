from django.db import models
from django import forms


class MoneyFormField(forms.CharField):

    def __init__(self, *args, **kwargs):
        self.precision = 100
        self.precision_number = 2
        super(MoneyFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = value.replace(',', '.')

        try:
            value = float(value)
        except ValueError:
            raise ValidationError(_('Field must be float number (ex. 125.55)'))

        test = value * self.precision
        if int(test) != test:
            raise ValidationError(_('Value precision -- maximum %s digits') % self.precision_number)

        return value



class MoneyField(models.IntegerField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, precision=2, *args, **kwargs):
        self.precision = 10 ** precision
        self.precision_number = precision
        super(MoneyField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value == None:
            return value

        if type(value) in (int, long):
            return float(value) / self.precision
        else:
            return float(value)
    
    def get_prep_value(self, value):
        db_value = float(value) * self.precision
        if db_value != int(db_value):
            raise ValueError()
        
        return int(db_value)

    def formfield(self, **kwargs):
        kwargs['form_class'] = MoneyFormField
        ff = super(MoneyField, self).formfield(**kwargs)
        
        ff.precision = self.precision
        ff.precision_number = self.precision_number
        
        return ff
    
    def contribute_to_class(self, cls, name):
        def getter(self):
            return int(getattr(self, name) * 100)
        cls.add_to_class('%s_natural' % name, getter)
        
        super(MoneyField, self).contribute_to_class(cls, name)
