from django.urls import path, include
from django.conf.urls import url
from git_auth.views import (
    GitHubVerifyView,
    GitHubUserReposView,
    GitHubAppAccessTokenView,
    GitHubCloneReposView,
    GitHubSaveUserDataView,
    GitHubPushWHView,
)

urlpatterns = [
    url(r'^verify', GitHubVerifyView.as_view(), name='verify'),
    url(r'^save-user-data', GitHubSaveUserDataView.as_view(), name='save-user-data'),
    url(r'^user-app-token', GitHubAppAccessTokenView.as_view(), name='user-app-token'),
    url(r'^user-repos', GitHubUserReposView.as_view(), name='user-repos'),
    url(r'^clone-repo', GitHubCloneReposView.as_view(), name='clone-repo'),
     url(r'^push-wh', GitHubPushWHView.as_view(), name='push-wh'),
]