from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import (RefreshToken,
                                             TokenError,
                                             OutstandingToken,
                                             BlacklistedToken)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
