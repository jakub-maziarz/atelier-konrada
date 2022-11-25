from .base import *

SECRET_KEY = 'django-insecure-bk+n1%0j#%k6bo(pva7d00o+lykdy$am-^@#z1b#ivh@-&=z5r'

DEBUG = True

ALLOWED_HOSTS = ['*']

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'

STATIC_URL = 'static/'

MEDIA_URL = '/images/'

MEDIA_ROOT = BASE_DIR / 'shop/static/shop'