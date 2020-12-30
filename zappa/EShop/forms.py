from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import EshopUser, Item


class EshopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = EshopUser
        fields = 'email',


class EshopUserChangeForm(UserChangeForm):
    class Meta:
        model = EshopUser
        fields = 'email',


class ItemChangeForm(forms.ModelForm):
    redeem = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['redeem'].initial = bool(kwargs['instance'].redeemed_by)
    class Meta:
        model = Item
        fields = '__all__'
