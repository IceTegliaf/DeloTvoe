import datetime
from pytils import numeral
from django.utils.translation import ugettext
from django.conf import settings
from django.utils.dateformat import format

def human_date(var):
    if not var:
        return var
    
    import datetime
    from pytils import numeral
#    numeral.choose_plural(amount, variants) 
    assert isinstance(var, (datetime.date, datetime.datetime)), "Wrong type %s " % type(var)
    now = datetime.date.today()
    #check today:
    if var.year==now.year and var.month==now.month and var.day==now.day:
        return ugettext("today")
    else:
        if var.year==now.year:
            if var.month==now.month:
                if var.day==now.day-1:
                    if isinstance(var, datetime.datetime):
                        return ugettext("yesterday in") + format(var, " H:i")
                    return ugettext("yesterday in")
                
                if var.day==now.day+1:
                    if isinstance(var, datetime.datetime):
                        return ugettext("tomorrow in") + format(var, " H:i")
                    return ugettext("tomorrow in")
                
                
                dd=now.day-var.day
                if dd<=7 and dd>=0:
                    return ("%s" % dd)+" " + numeral.choose_plural(dd,
                                                (ugettext("1 day ago"),
                                                 ugettext("2 days ago"), 
                                                 ugettext("5 days ago"))
                                                )
                if dd>=-7 and dd<0:
                    return ugettext("through")+(" %s" % (dd*-1))+" "+ numeral.choose_plural(dd*-1,
                                                (ugettext("1 day"),
                                                 ugettext("2 days"), 
                                                 ugettext("5 days"))
                                                )
            
                
            return format(var, "d M.").lower()
    return format(var, "d M y").lower()

def human_datetime(var):
    if not var:
        return var
        
    assert type(var) == datetime.datetime, "Wrong type %s " % type(var)
    now = datetime.datetime.today()
    #check today:
    if var.year==now.year and var.month==now.month and var.day==now.day:
        delta=now-var
        min = int(delta.seconds/60)
        if min==0:
            return ugettext("now")
        if min<60 and min>0:
            return ("%s" % min)+" "+ numeral.choose_plural(min,
                                        (ugettext("1 minute ago"),
                                         ugettext("2 minutes ago"), 
                                         ugettext("5 minutes ago"))
                                        )            
        if min>-60 and min<0:
            return ugettext("through")+(" %s" % min*-1)+" "+ numeral.choose_plural(min*-1,
                                        (ugettext("1 minute"),
                                         ugettext("2 minutes"), 
                                         ugettext("5 minutes"))
                                        )            

        if min>=60 and min<120:
            return ugettext("hour ago")
        
        if min>=-120 and min<-60:
            return ugettext("through hour")
        
        
        if min>=120 and min<=600:
            hour = int(min/60)
            return ("%s" % hour)+" "+ numeral.choose_plural(hour,
                                        (ugettext("1 hour ago"),
                                         ugettext("2 hours ago"), 
                                         ugettext("5 hours ago"))
                                        )
            
        if min>=-600 and min<=-120:
            hour = int(min/60)
            return ugettext("through")+(" %s" % hour)+" "+ numeral.choose_plural(hour,
                                        (ugettext("1 hour"),
                                         ugettext("2 hours"), 
                                         ugettext("5 hours"))
                                        )        

        return format(var, settings.TIME_FORMAT)
    
    return human_date(var)