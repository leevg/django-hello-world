from django.db import models
from django.db.models.signals import post_save, post_delete
from django.db.utils import DatabaseError
from django.contrib.auth.models import User
# Create your models here.


CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)


class UserInfo(User):
    date_of_birth = models.DateField()
    bio = models.TextField(blank=True)
    jabber = models.CharField(max_length=50, blank=True)
    skype = models.CharField(max_length=50, blank=True)
    other_contacts = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos', blank=True, null=True)


class RequestInfo(models.Model):
    method = models.CharField(max_length=5)
    path = models.CharField(max_length=70)
    time = models.DateTimeField(auto_now_add=True)
    priority = models.SmallIntegerField(default=1, choices=CHOICES)

    def __unicode__(self):
        return u"%s %s%s" % (self.method.upper(), self.path, self.query)

    class Meta():
        ordering = ["-priority", "time"]


class ModelLog(models.Model):
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'

    created_at = models.DateTimeField(auto_now=True)
    app_label = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    action = models.CharField(max_length=50)

    @classmethod
    def log(cls, instance, action):
        # exclude ModelLog changes from log
        if not isinstance(instance, ModelLog):
            try:
                entry = ModelLog(
                    app_label=instance._meta.app_label,
                    model_name=instance.__class__.__name__,
                    action=action
                )
                entry.save()
            except DatabaseError:
                pass


def log_update_create(sender, instance, created, **kwargs):
    ModelLog.log(instance,
                 ModelLog.ACTION_CREATE if created else
                 ModelLog.ACTION_UPDATE)


def log_delete(sender, instance, **kwargs):
    ModelLog.log(instance, ModelLog.ACTION_DELETE)

post_save.connect(log_update_create, dispatch_uid='log_update_create')
post_delete.connect(log_delete, dispatch_uid='log_delete')
