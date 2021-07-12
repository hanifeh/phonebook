from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

# Create your models here.

phone_regex = RegexValidator(regex='^09[0-9]{9}$', message='phone number invalid')


class MyUser(models.Model):

    first_name = models.CharField(max_length=50, verbose_name=_('first name'))
    last_name = models.CharField(max_length=50, verbose_name=_('last name'))
    phone_number = models.CharField(validators=[phone_regex], max_length=11, verbose_name=_('phone number'))
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        unique_together = [['phone_number', 'user']]
