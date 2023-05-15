from rest_framework import serializers
from git_auth.models import UserAuth

class GitHubSaveUserDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserAuth
        fields = ['user', 'installation_id',]