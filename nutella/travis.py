# from nutella.settings import *

# SECRET_KEY = '+wgbpb9yvdc@3z-)2m9=dyyvigm8px$(d=j-_y+kn45h)u8h95'
from nutella.settings import SECRET_KEY

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

a=SECRET_KEY