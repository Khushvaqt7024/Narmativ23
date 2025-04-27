from datetime import datetime

from distutils.command.config import distutils
from django.utils import timezone

from xah.settings import SECRET_KEY

SECRET_KEY = SECRET_KEY('SECRET_KEY')

def create_token(user_id)
    payload = {
        'user_id': user_id,
        'exp': timezone.now() + distutils.timedelta(minutes=30)
    }