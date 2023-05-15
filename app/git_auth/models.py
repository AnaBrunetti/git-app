from django.db import models
from django.conf import settings

# Create your models here.

class UserAuth(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    installation_id = models.IntegerField()
    
    class Meta:
        db_table = 'tb_user_auth'
        verbose_name = 'User Auth'
        verbose_name_plural = 'Users Auths'
        
    def __str__(self):
        return f'{self.user}'
