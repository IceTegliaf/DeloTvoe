"""
author:Kovalenko Pavel (pavel@bitrain.ru)
"""
from apps.xml_menu.reader import Menu

class CPXMPMenu(object):
    def __init__(self, req):
        self.req = req
    
    def root(self):
        if not hasattr(self, "_menu"):
            self._menu = Menu(self.req)
            self._menu.load_from_xml()
            self._menu.select(self.req.path)
        return self._menu.root_item
    
    def get_selected(self):
        for item in self.root():
            if item.selected:
                return item
        return None;
    


def cp_xml_menu(request):
    return { 'cp_xml_menu': CPXMPMenu(request) }