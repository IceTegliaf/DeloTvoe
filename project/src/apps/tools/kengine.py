from apps.kengine.module import BaseModule


class Module(BaseModule):
    
    priority = 100
    
    def configurate(self, conf):
        #settings
        conf.add_app("apps.tools")
