from django.contrib import admin

from .forms import ProfileForm
# from .forms import MessagesForm
from .models import Profile
from .models import Messages


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'external_id',
        'name'
    )
    form = ProfileForm


@admin.register(Messages)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'profile',
        'text',
        'created_at',
    )
#     form = MessagesForm
