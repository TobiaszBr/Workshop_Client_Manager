from decouple import config

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "railway",
        "USER": "postgres",
        "PASSWORD": config("EXTERNAL_POSTGRESQL_DATABASE_PASSWORD"),
        "HOST": "containers-us-west-50.railway.app",
        "PORT": "6557",
    }
}
