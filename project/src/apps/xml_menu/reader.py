"""
author:Kovalenko Pavel (pavel@bitrain.ru)  
"""
from xml.dom import minidom, Node
import os
from django.core.urlresolvers import reverse, get_urlconf
import re
from django.conf import settings
from apps.tools.class_loader import get_class_by_string
from apps.xml_menu.patch_urlresolvers import resolve2
from apps.tools.shortcuts import get_settings



DEFAULT_MENU = os.path.join(settings.PROJECT_ROOT,get_settings("XML_MENU_FILE", os.path.join("settings","menu.xml")))
root_item=None

def get_attr(node, attr_name):
    for attr in node.attributes.items():
        if attr[0]==attr_name:
            return attr[1]
    raise Exception('Unknown attribute "%s" in "%s"' % (attr_name, node.tagName))


def safe_get_attr(node, attr_name):
    for attr in node.attributes.items():
        if attr[0]==attr_name:
            return attr[1]
    return None


class View(object):
    
    def __init__(self):
        self.pattern = ''
        self.func_name=''
        self.kwargs = {}
        self.ne_kwargs = {}
        
    def _load(self, node):
        try:
            self.pattern = get_attr(node, 'name')        
        except:
            pass
        try:
            self.func_name = get_attr(node, 'function')
        except:
            pass

        for child in node.childNodes:
            if child.nodeType==Node.ELEMENT_NODE:
                #value_ne                
                ne=safe_get_attr(child, 'value_ne')
                if ne:
                    self.ne_kwargs[str(child.tagName)] = get_attr(child, 'value_ne')
                else:
                    self.kwargs[str(child.tagName)] = get_attr(child, 'value')
                
    def exec_func(self,view_name, kwargs):        
        pos = self.func_name.rfind(".")
        app = self.func_name[:pos]
        func_name = self.func_name[pos+1:]
        mod = __import__(app,[],[],[func_name])
        if hasattr(mod, func_name):
            func = getattr(mod, func_name)
            return func(view_name, kwargs)
        raise Exception("Error loading 'function': %s" % self.func_name)
                
    def match(self, view_name, kwargs):
        if self.pattern:
            p = re.match(self.pattern, view_name)
            if p:
                for aname in self.ne_kwargs:
                    if aname in kwargs and self.ne_kwargs[aname]==kwargs[aname]:
                        return False                
                for aname in self.kwargs:
                    if aname in kwargs and self.kwargs[aname]!=kwargs[aname]:
                        return False
                if self.func_name:
                    return self.exec_func(view_name, kwargs) 
                return True
        else:
            if self.func_name:
                return self.exec_func(view_name, kwargs)
        
        return False
        
class Item(object):
    
    
    def __init__(self, req):
        self.name=''
        self.childs=[]
        self.url_name=''
        self.url_href=''
        self.url_attrs={}
        self.views=[]
        self.selected=False
        self.req = req

    __unicode__ = lambda self: self.name
    
    def selected_item(self):
        for item in self:
            if item.selected:
                return item
        return None
    
    def __iter__(self):
        for child in self.childs:
            if child.can_access():
                yield child
            
    def _load(self, node):
        for attr in node.attributes.items():
            setattr(self, attr[0], attr[1])
            
        for child in node.childNodes:
            if child.nodeType==Node.ELEMENT_NODE:
                if child.tagName=='childs':
                    self._load_childs(child)
                
                if child.tagName=='url':
                    self._load_urls(child)
    
                if child.tagName=='view':
                    self._load_view(child)


    def _load_childs(self, childs):
        for child in childs.childNodes:
            if child.nodeType==Node.ELEMENT_NODE and child.tagName=='item':
                item = Item(self.req)
                item._load(child)          
                self.childs.append(item)

    def _load_urls(self, url):
        self.url_name = safe_get_attr(url, 'name')
        self.url_href = safe_get_attr(url, 'href')
        assert self.url_href or self.url_name, "xml_menu:url mast have 'name' or 'href' attribute" 
        self.url_attrs={}
        for url_attr in url.childNodes:
            if url_attr.nodeType==Node.ELEMENT_NODE:
                call_function = safe_get_attr(url_attr, 'call_function')
                if call_function:
                    self.url_attrs[str(url_attr.tagName)]= get_class_by_string(call_function)
                else:
                    self.url_attrs[str(url_attr.tagName)]=get_attr(url_attr, 'value')

    def _load_view(self, view_node):
        view = View()
        view._load(view_node)        
        self.views.append(view)

                
    def get_absolute_url(self):
        if self.url_href:
            return self.url_href
        if self.url_name:
            #call all callable value and make new dict
            kwargs = dict(map(lambda key: \
                         (key, self.url_attrs[key](self.req) \
                            if callable(self.url_attrs[key]) \
                            else self.url_attrs[key] ),
                            self.url_attrs))
            #get real url with keywords arguments 
            return reverse(self.url_name, kwargs=kwargs)
        else:
            if len(self.childs)>0:
                return self.childs[0].get_absolute_url()
        return "#MenuUrlNotFound"
    
    def select(self, url_names, view_name, view_kwargs):
        for child in self:
            if child.select(url_names, view_name, view_kwargs):
                self.selected=True
                return True
                
        if url_names:
            if self.url_name in url_names:
                self.selected=True
                return True
                
        for view in self.views:
            if view.match(view_name, view_kwargs):                
                self.selected=True
                return True        
        return False
    
    def can_access(self):
        #find linked object
        resolve_value = resolve2(self.get_absolute_url())
        if resolve_value:
            ret, args, view_kwargs = resolve_value
            if hasattr(ret, '_callback') and callable(ret._callback) and hasattr(ret._callback, "xml_menu__can_access"):
                return ret._callback.xml_menu__can_access(self.req.user)
        return True
    
    def get_selected(self):
        for item in self:
            if item.selected:
                return item
        return None;
    
    
class Menu(object):
    
    def __init__(self, req):
        self.root_item = None
        self.req = req
    
    def load_from_xml(self):
        f = open(os.path.join(settings.PROJECT_ROOT, DEFAULT_MENU), "r")
        xml_document = "".join(f.readlines())
        f.close()
        doc = minidom.parseString(xml_document)
        for child in doc.childNodes:
            if child.nodeType==Node.ELEMENT_NODE and child.tagName=='item':
                self.root_item = Item(self.req)
                self.root_item._load(child)
                
    def select(self, url, ignore_resolve_error=False):
        try:
            resolve_value =  resolve2(url)
        except:
            resolve_value = None
        if not resolve_value:
            if not ignore_resolve_error and not self.req.xml_menu_ignore_resolve_error:
                raise Exception("xml_menu: can't resolve view for select current menu item, from URL\nURL: %s" % url)
            else:
                return False                
        
        ret, args, view_kwargs = resolve_value
        url_names = None
        
        if hasattr(ret, '_callback_str'):
            url_view_name =  ret._callback_str
        
        elif hasattr(ret, '_callback') and callable(ret._callback):
            if hasattr(ret._callback, "xml_menu__selected_url_names"):
                url_names = ret._callback.xml_menu__selected_url_names()
            url_view_name = "%s.%s" % (type(ret._callback).__module__,type(ret._callback).__name__)
        else:
            raise Exception("Can not connect to URL with view\nURL: %s" % url) 

        for item in self.root_item:
            if item.select(url_names, url_view_name, view_kwargs):
                return True
        return False
                
#    def test(self):
#        from django.template.loader import render_to_string
#        return render_to_string('xml_menu/test.html', {'root': self.root_item})

        

