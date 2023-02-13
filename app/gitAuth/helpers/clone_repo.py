import sys
import os
from django.conf import settings

def clone(user_token, repo):
    path  = f"{settings.BASE_DIR}\gitAuth\projects"
    clone = f"git clone https://x-access-token:{user_token}@github.com/{repo}.git" 

    # os.system("sshpass -p your_password ssh user_name@your_localhost")
    try:
        os.chdir(path) # Specifying the path where the cloned project needs to be copied
        os.system(clone) # Cloning
        path = path.replace('\\', '/')
        return "The project has been successfully cloned!"
    except Exception as error:
        return error