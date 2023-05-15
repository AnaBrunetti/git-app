from django.shortcuts import render

# Create your views here.
from rest_framework import views
from rest_framework.response import Response
from django.conf import settings
import requests
from django.shortcuts import render
from git_auth.models import UserAuth
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from rest_framework import status
from django.utils import timezone
import json

User = get_user_model()

def get_jwt():
    with open(f"{settings.BASE_DIR}\git_auth\confs\github-jwt.json", "r") as file:
        jwt = json.load(file)
    return jwt['jwt']

def get_repos(user):
    user_auth = UserAuth.objects.get(user=user)
    headers = {
        'Authorization': f'Bearer {user_auth.access_token}',
        'Accept': 'application/vnd.github+json'
    }
    repos = requests.get('https://api.github.com/user/repos', headers=headers).json()
    return repos

def refresh_token(user_auth):
        url = f"https://github.com/login/oauth/access_token?client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}&refresh_token={user_auth.refresh_token}&grant_type=refresh_token"
        headers = {'Accept': 'application/json'}
        response = requests.post(url, headers=headers).json()
        create_or_update_user_auth(user_auth.user, response)

def create_or_update_user_auth(user, response):
    if UserAuth.objects.filter(user=user).exists():
        auth = UserAuth.objects.get(user=user)
        auth.refresh_token=response.get('refresh_token')
        auth.refresh_token_expires_in=int(response.get('refresh_token_expires_in'))
        auth.access_token=response.get('access_token')
        auth.access_token_expires_in=int(response.get('expires_in')) 
        auth.save()
    else:
        auth = UserAuth.objects.create(
            user=user,
            refresh_token=response.get('refresh_token'),
            refresh_token_expires_in=int(response.get('refresh_token_expires_in')),
            access_token=response.get('access_token'),
            access_token_expires_in=int(response.get('expires_in'))
        )
    return auth
  
def verify_user_auth(user):
    try:
        user_auth = UserAuth.objects.get(user=user)
        if user_auth.updated_at + timedelta(seconds=user_auth.refresh_token_expires_in) < timezone.now():
           return False
        elif user_auth.updated_at + timedelta(seconds=user_auth.access_token_expires_in) < timezone.now():
            refresh_token(user_auth)
            return True
        else:
            return True
    except Exception as error:
        print(error)
        return False
    
def get_installation(user):
    user_auth = UserAuth.objects.get(user=user)
    url = f"https://api.github.com/user/installations/{user_auth.installation_id}/repositories"
    headers = {
        'Authorization': f'Bearer {user_auth.access_token}',
        'Accept': 'application/vnd.github+json'
    }
    installations = requests.get(url, headers=headers).json()
    return(installations)


class GitHubLoginView(views.APIView):
    
    def get(self, request):
        return render(request, 'git_login.html')


# class GitHubRequestTokenView(views.APIView):
    
#     def post(self, request):
#         url = f"https://github.com/login/oauth/access_token?client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}&code={request.query_params.get('code')}"
#         headers = {'Accept': 'application/json'}
#         response = requests.post(url, headers=headers).json()
#         if response.get('error'):
#             return Response(response, status=status.HTTP_400_BAD_REQUEST)
#         create_or_update_user_auth(request.user, response)
#         return Response(response)

    
class GitHubReposView(views.APIView):
    
    def get(self, request):
        if verify_user_auth(request.user):
            return Response(get_repos(request.user))
        return Response({'message': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
# class GitHubInstallationView(views.APIView):
    
#     def get(self, request):
#         if verify_user_auth(request.user):
#             return Response(get_installation(request.user))
#         return Response({'message': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
class GitHubRequestTokenView(views.APIView):
    
    def post(self, request):
        url = f"https://github.com/login/oauth/access_token?client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}&code={request.query_params.get('code')}"
        headers = {'Accept': 'application/json'}
        response = requests.post(url, headers=headers).json()
        if response.get('error'):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        auth = create_or_update_user_auth(request.user, response)
        auth.installation_id = int(request.query_params.get('installation_id'))
        auth.save()
        return Response(response)
    
    
class GitHubAppInstallationView(views.APIView):
    
    def get(self, request):
        url = f"https://api.github.com/app/installations"
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {get_jwt()}',
        }
        response = requests.post(url, headers=headers).json()
        return Response(response)
    
    