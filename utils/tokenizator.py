import jwt
from datetime import datetime, timedelta
from rest_framework_simplejwt import tokens
from traveler import settings
from accounts.models import User

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_token(user_id: int) -> dict:
    user = User.objects.get(pk=user_id)
    token = tokens.RefreshToken.for_user(user)
    return str(token.access_token)

