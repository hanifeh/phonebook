from django import forms
from django.core.exceptions import ValidationError

from . import models


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UserForm, self).__init__(*args, **kwargs)

    # def clean_phone_number(self):
    #     phone_number = self.cleaned_data['phone_number']
    #     if models.MyUser.objects.filter(user=self.user, phone_number=phone_number).exists():
    #         raise ValidationError('phone number already exist. ')
    #     return phone_number

    class Meta:
        model = models.MyUser
        fields = [
            'first_name',
            'last_name',
            'phone_number',
        ]


class EditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.MyUser
        fields = [
            'first_name',
            'last_name',
            'phone_number',
        ]
