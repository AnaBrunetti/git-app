#!/usr/bin/env python3
import jwt
import time
import sys
from django.conf import settings
import json

def create_token():
    # Open PEM
    with open(f"{settings.BASE_DIR}\git_auth\confs\pem-key.private-key.pem", "rb") as pem_file:
        signing_key = jwt.jwk_from_pem(pem_file.read())

    # Get the App ID
    app_id = 291547

    payload = {
        # Issued at time
        'iat': int(time.time()),
        # JWT expiration time (10 minutes maximum)
        'exp': int(time.time()) + 600,
        # GitHub App's identifier
        'iss': app_id
    }

    # Create JWT
    jwt_instance = jwt.JWT()
    encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')

    jwt_token = {
        "jwt": encoded_jwt
    }

    json_object = json.dumps(jwt_token, indent=1)

    with open(f"{settings.BASE_DIR}\git_auth\confs\github-jwt.json", "w+") as file:
            file.write(json_object)