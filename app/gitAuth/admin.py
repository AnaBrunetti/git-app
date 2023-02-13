from django.contrib import admin
from gitAuth.models import UserAuth

# Register your models here.

@admin.register(UserAuth)
class UserAuthAdmin(admin.ModelAdmin):
    pass
