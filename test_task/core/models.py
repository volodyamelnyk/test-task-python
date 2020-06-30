from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .constants import domain_or_ip_regex, INCORRECT_DOMAIN_OR_IP
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
from django.core.mail import send_mail
from test_task import settings

# Create your models here.


class Request(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=False)
    description = models.TextField()
    ip = models.GenericIPAddressField()
    is_blocked = models.BooleanField(default=False)
    domain_or_ip = models.TextField(
        validators=[
            RegexValidator(
                regex=domain_or_ip_regex,
                message=INCORRECT_DOMAIN_OR_IP
            ),
        ])

    class Meta:
        db_table = 'requests'


class BlockedDomain(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    request = models.ForeignKey('Request', on_delete=models.CASCADE)

    class Meta:
        db_table = 'blocked_domains'


@receiver(post_save, sender=BlockedDomain)
def post_save_confirm_code(sender, **kwargs):
    send_mail(
        'Test task message',
        'Domain or IP {0} was blocked!'.format(
            kwargs['instance'].request.domain_or_ip),
        settings.DEFAULT_FROM_EMAIL,
        [kwargs['instance'].request.email],
        fail_silently=False,
    )
    Request.objects.filter(
        uuid=kwargs['instance'].request.uuid).update(is_blocked=True)
