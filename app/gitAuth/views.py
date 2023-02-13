from django.shortcuts import render

# Create your views here.
from rest_framework import views
from rest_framework.response import Response
from django.conf import settings
import requests
from gitAuth.models import UserAuth
from django.contrib.auth import get_user_model
import json
from gitAuth.helpers.generate_jwt import create_token
from gitAuth.helpers.clone_repo import clone
from gitAuth.serializers import GitHubSaveUserDataSerializer

User = get_user_model()

def create_or_update_user_installation(request):
    if UserAuth.objects.filter(user=request.user).exists():
        user = UserAuth.objects.get(user=request.user)
        user.installation_id = request.data['installation_id']
        user.save()
    else:
        user = UserAuth.objects.create(
            user=request.user,
            installation_id = request.data['installation_id']
        )
    return user

def get_installation_headers():
    headers = {
        'Authorization': f'Bearer {make_jwt()}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    return headers

def get_jwt():
    with open(f"{settings.BASE_DIR}\gitAuth\confs\github-jwt.json", "r") as file:
        jwt = json.load(file)
    return jwt['jwt']

def make_jwt():
    create_token()
    with open(f"{settings.BASE_DIR}\gitAuth\confs\github-jwt.json", "r") as file:
        jwt = json.load(file)
    return jwt['jwt']
  
def verify_user_auth(user):
    ### TODO: MAKE ATOMIC ###
    if UserAuth.objects.filter(user=user).exists():
        user_auth = UserAuth.objects.get(user=user)
        url = f"https://api.github.com/app/installations/{user_auth.installation_id}"
        headers = get_installation_headers()
        print(headers)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True        
    return False
    
def get_app_access_token(user):
    ### TODO: MAKE ATOMIC ###
    user_auth = UserAuth.objects.get(user=user)
    url = f"https://api.github.com/app/installations/{user_auth.installation_id}/access_tokens"
    headers = get_installation_headers()
    response = requests.post(url, headers=headers).json()
    return(response)

def get_user_repos(user):
    url = f"https://api.github.com/installation/repositories"
    headers = {
        'Authorization': f'Bearer {get_app_access_token(user)["token"]}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    repos = requests.get(url, headers=headers).json()
    return(repos['repositories'])

def get_clone_user_repos(request):
    return(clone(get_app_access_token(request.user)['token'], request.data['repo']))


class GitHubSaveUserDataView(views.APIView):
    serializer = GitHubSaveUserDataSerializer
    
    def post(self, request):
        try:
           user = create_or_update_user_installation(request)
           response = self.serializer(user)
           return Response(response.data)
        except Exception as error:
            return Response(error)
    
class GitHubVerifyView(views.APIView):
    
    def get(self, request):
        try:
            response = verify_user_auth(request.user)
            return Response(response)
        except Exception as error:
            return Response(error)

class GitHubAppAccessTokenView(views.APIView):
    
    def get(self, request):
        try:
            response = get_app_access_token(request.user)
            return Response(response)
        except Exception as error:
            return Response(error)

class GitHubUserReposView(views.APIView):
    
    def get(self, request):
        try:
            response = get_user_repos(request.user)
            return Response(response)
        except Exception as error:
            return Response(error)
    
class GitHubCloneReposView(views.APIView):
    
    def post(self, request):
        try:
            response = get_clone_user_repos(request)
            return Response(response)
        except Exception as error:
                return Response(error)