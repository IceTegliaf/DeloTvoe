from apps.kengine.module import BaseModule

class Module(BaseModule):
    
    def configurate(self, conf):
        #settings
        conf.add_app("apps.compressor")
        conf.add_middleware("apps.compressor.middleware.CompressorMiddleware")
        
