from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")

GOOGLE_OAUTH_CALLBACK_URL = "http://localhost:8000/oauth/google/callback"

GOOGLE_OAUTH_USER_PROFILE = "https://www.googleapis.com/oauth2/v1/userinfo"

GOOGLE_OAUTH_TOKEN_URI =  "https://oauth2.googleapis.com/token"
GOOGLE_OAUTH_AUTH_URI =  "https://accounts.google.com/o/oauth2/auth"
