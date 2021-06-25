from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

phone_regex = RegexValidator(regex='^09[0-9]{9}$', message='phone number invalid')


class MyUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(validators=[phone_regex], max_length=11)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        unique_together = [['phone_number', 'user']]
