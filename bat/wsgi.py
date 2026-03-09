import os
from pathlib import Path

_env = Path(__file__).resolve().parent.parent / '.env'
if _env.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env)
    except ImportError:
        pass

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bat.settings')
application = get_wsgi_application()
