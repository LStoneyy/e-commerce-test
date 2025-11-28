from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
