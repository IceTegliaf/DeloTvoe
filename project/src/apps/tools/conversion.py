import re
import types


RE_CC_TO_US = re.compile(r"([A-Z][a-z]*)")

def CamelCase_to_under_score(name):
    l = RE_CC_TO_US.split(name)
    try:
        while True:
            l.remove("")
    except ValueError:
        pass
    return "_".join(l).lower()

def cc2us(data):
    if isinstance(data, types.DictionaryType):
        out={}
        for key in data:
            out[CamelCase_to_under_score(key)] = data[key]
        return out
    
    return CamelCase_to_under_score(data)



def prepare_const(*args):
    return "_".join(args).replace(".", "_").upper()


def python_to_string(value):
    if isinstance(value, types.StringTypes):
        return "\"%s\"" % value
    return value