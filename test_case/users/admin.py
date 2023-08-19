from django.contrib import admin
from .models import *
# Register your models here.

class UserView(admin.ModelAdmin):
    list_display = ('phone_number', 'invite_code','referred_by')

    def get_fields(self, request, obj=None):
        return ['phone_number', 'invite_code','referred_by']
    

# admin.site.register(User)
admin.site.register(User,UserView)