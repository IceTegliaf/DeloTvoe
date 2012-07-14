from django.core.management.base import NoArgsCommand
from apps.tools.check_settings import run_chekers
import sys


class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        if run_chekers():
            sys.exit(-1)
            
    
    