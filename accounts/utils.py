import requests
from django.conf import settings

def get_google_user_info(code):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',

    }
    r = requests.post(token_url, data=data)
    r.raise_for_status()
    tokens = r.json()

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {'Authorization': f"Bearer {tokens['access_token']}"}
    r2 = requests.get(userinfo_url, headers=headers)
    r2.raise_for_status()
    return r2.json()
