from jsonrpc import jsonrpc_method
from apps.static_blocks.models import Block
from apps.tools.jrpc import to_json
from django.contrib.sites.models import Site


@jsonrpc_method("static_blocks.get(address=String)")
def get(req, address):
    block, created = Block.objects.get_or_create(address = address, site = Site.objects.get_current())
    if created:
        block.title = address
        block.save()
    
    return to_json(block, ('content','title','use_title'))
        