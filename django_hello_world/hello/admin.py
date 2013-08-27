from django.contrib import admin
from models import UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']

admin.site.register(UserInfo, UserInfoAdmin)
