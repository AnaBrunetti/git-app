from django.contrib import admin
from git_auth.models import UserAuth

# Register your models here.

@admin.register(UserAuth)
class UserAuthAdmin(admin.ModelAdmin):
    pass
