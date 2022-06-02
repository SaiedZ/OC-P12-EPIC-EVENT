"""
Views for the authentication API.
"""

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import (RefreshToken,
                                             TokenError,
                                             OutstandingToken,
                                             BlacklistedToken)
from rest_framework.response import Response


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
    """Allow users to logout from all devices."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Post methode to handle logging out.

        Will get all the tokens related to the request user and blacklist them.

        Args:
            request: Http request

        Returns:
            response: Http response
        """
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
