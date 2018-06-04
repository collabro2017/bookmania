from django.contrib.staticfiles.management.commands.collectstatic import Command as BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        settings.STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        super(Command, self).__init__(*args, **kwargs)