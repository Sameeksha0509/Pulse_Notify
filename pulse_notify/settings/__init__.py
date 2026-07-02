import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')

module_name = os.getenv('DJANGO_SETTINGS_MODULE', 'pulse_notify.settings.local')
if 'production' in module_name:
    from .production import *
else:
    from .local import *
