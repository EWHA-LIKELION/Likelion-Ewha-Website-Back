from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings

def verify_google_id_token(raw_id_token: str) -> dict:
    req = google_requests.Request()
    payload = id_token.verify_oauth2_token(
        raw_id_token,
        req,
        settings.GOOGLE_OAUTH_CLIENT_ID,
    )
    return payload
