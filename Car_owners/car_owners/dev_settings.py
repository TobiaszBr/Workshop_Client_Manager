import os

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "railway",
        "USER": "postgres",
        "PASSWORD": os.getenv("EXTERNAL_POSTGRESQL_DATABASE_PASSWORD"),
        "HOST": "containers-us-west-50.railway.app",
        "PORT": "6557",
    }
}
