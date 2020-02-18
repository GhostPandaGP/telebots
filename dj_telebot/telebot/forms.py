from django import forms

from .models import Profile
from .models import Messages


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'external_id',
            'name',
        )
        widgets = {
            'name': forms.TextInput,
        }


# class MessagesForm(forms.ModelForm):
#
#     class Meta:
#         model = Messages
#         fields = (
#             'profile',
#             'text',
#             'created_at',
#         )
#         widgets = {
#             'profile': forms.TextInput,
#         }