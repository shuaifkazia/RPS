import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from users.models import User


class Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request)
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.decode('utf-8').split(' ')
            if prefix.lower() != 'bearer':
                return None
            
        
            decoded = jwt.decode(token, 'QZTD', algorithms=["HS256"])
     
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        try:
            user = User.objects.get(id=decoded['user']['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, token)
