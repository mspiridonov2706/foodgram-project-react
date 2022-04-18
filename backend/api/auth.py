from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from .serializers import AuthCustomTokenSerializer
from recipes.models import User


class CustomAuthToken(ObtainAuthToken):

    def post(self, request):
        serializer = AuthCustomTokenSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            data = {'auth_token': token.key}
            return Response(data=data, status=status.HTTP_201_CREATED)
        raise AuthenticationFailed()


class CustomLogoutToken(ObtainAuthToken):

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            Token.objects.filter(user=user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise AuthenticationFailed()
