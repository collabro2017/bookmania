from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.models import AbstractUser
from django.db import models
from publisher.models import Publisher, Book
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from time import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


def profile_pic_path(instance, filename):
    timestamp = time()
    return 'profile_pics/{}/{}_{}'.format(instance.id, timestamp, filename)


class User(AbstractUser):
    PUBLISHER = 'publisher'
    STAFF = 'staff'
    READER = 'reader'
    USER_TYPES = [
        (PUBLISHER, PUBLISHER),
        (STAFF, STAFF),
        (READER,READER),
    ]

    ENGLISH = 'english'
    SPANISH = 'spanish'
    LANGAUGE_CHOICES = [
        (ENGLISH,ENGLISH),
        (SPANISH,SPANISH)
    ]
    
    FREE = 'free'
    PREMIUM = 'premium'
    BETA = 'beta'

    SUBSCRIPTION_TYPES = [
        (FREE,FREE),
        (PREMIUM,PREMIUM),
        (BETA,BETA)
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default=PUBLISHER)
    phone = models.CharField(max_length=10, default='')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, default=None)
    profile_pic = models.ImageField(upload_to=profile_pic_path, null=True, default=None)
    profile_pic_thumbnail = ProcessedImageField(upload_to=profile_pic_path,
                                          processors=[ResizeToFill(300, 300)],
                                          format='JPEG',
                                          options={'quality': 80},
                                          null=True,
                                          default=None)

    #for readers:
    age = models.PositiveIntegerField(blank=True,null=True)
    native_langauge = models.CharField(max_length=20, choices=LANGAUGE_CHOICES, default=ENGLISH)
    secondary_language = models.CharField(max_length=20, choices=LANGAUGE_CHOICES, default=SPANISH)
    name = models.CharField(max_length=20, null=True, blank=True)
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, default=FREE)

    def get_profile_pic(self):
            if self.profile_pic_thumbnail:
                return self.profile_pic_thumbnail.url
            else:
                return staticfiles_storage.url('images/samples/no_profile_image.jpg')

    def get_best_name(self):
        if self.first_name:
            return '{} {}'.format(self.first_name, self.last_name).title()
        else:
            return self.username


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
