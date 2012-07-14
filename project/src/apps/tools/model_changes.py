from django.db import models


class ArgumentError(Exception):
    pass


def get_dict_from_object(obj):
    data={}
    for field in obj._meta.fields:
        try:
            data[field.name] = getattr(obj, field.name)
        except Exception:
            data[field.name] = None
    return data

def changed_FIELD(name):
    def check_changed(self):
        return getattr(self, name)!=self._start_data[name]
    return check_changed

def old_FIELD(name):
    def old(self):
        return self._start_data[name]
    return old


class CheckChangesModel(models.Model):
    forget_changes_on_save = True
    important_fields = []
    
    
    def __init__(self, *args, **kwargs):        
        super(CheckChangesModel, self).__init__(*args, **kwargs)
        self._start_data = get_dict_from_object(self)
        
        if not self.important_fields: #set all fields are important
            self.important_fields = [f.name for f in self._meta.fields]
        
        klass = type(self)
        if not hasattr(klass, '_init_functions'):
            klass._init_functions=True

            for key in self._start_data:
                setattr(klass,"changed_%s" % key, changed_FIELD(key))
                setattr(klass,"get_%s_old_value" % key, old_FIELD(key))

    def forget_changes(self):
        self._start_data = get_dict_from_object(self)
    forget_changes.alters_data = True
    
    def is_new(self):
        return not bool(self._start_data['id']) #TODO: change 'id' to pk_name
        
    
    def save(self, **kwargs):
        super(CheckChangesModel, self).save(**kwargs)
        if self.forget_changes_on_save:
            self.forget_changes()
        
    def changes_field_names(self, field_names=None):
        if not field_names:
            field_names = self.important_fields
        
        if not field_names:
            raise ArgumentError("Put values for %s.important_fields or use argument for function changes_field_names " % type(self))
        
        return [name for name in field_names if getattr(self, name)!=self._start_data[name] ]
 

    def check_changes(self, field_names=None):
        if self.is_new():
            return True
        
        if not field_names:
            field_names = self.important_fields
        
        if not field_names:
            raise ArgumentError("Put values for %s.important_fields or use argument for function check_changes " % type(self))
        
        for name in field_names:
            if getattr(self, name)!=self._start_data[name]:
                return True
        return False
    
      
    class Meta:
        abstract = True
