from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    GenericAPIView,
    UpdateAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .serializers import (
    UserSerializer,
    LoginSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
)

from .models import CustomUser
# Create your views here.


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class loginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        if serializer.is_valid():
            response = Response(
                {"User:": LoginSerializer(user).data}, status=status.HTTP_200_OK
            )
            response.set_cookie(
                key="access_token",
                value=access,
                httponly=True,
                secure=True,
                samesite="None",
            )  # Set HttpOnly cookie
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="None",
            )  # Set HttpOnly cookie
            return response

        return Response({serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)


class logoutView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        response = Response({"message": "Logout successful"}, status=200)

        # Instead of delete_cookie, overwrite with expired cookies
        # This ensures all parameters match the original cookie settings
        response.set_cookie(
            key="access_token",
            value="",
            httponly=True,
            secure=True,
            samesite="None",
            expires="Thu, 01 Jan 1970 00:00:00 GMT",  # Expire immediately
            max_age=0,  # Zero max age
        )
        response.set_cookie(
            key="refresh_token",
            value="",
            httponly=True,
            secure=True,
            samesite="None",
            expires="Thu, 01 Jan 1970 00:00:00 GMT",  # Expire immediately
            max_age=0,  # Zero max age
        )

        # Blacklist token
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                # Log the error but don't fail the logout
                print(f"Blacklist error: {str(e)}")

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        old_refresh_token = request.COOKIES.get("refresh_token")

        if old_refresh_token is None:
            return Response(
                {"detail": "Refresh token not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Decode refresh token (will fail if expired)
            old_token = RefreshToken(old_refresh_token)

            # Blacklist the old refresh token
            old_token.blacklist()

            user = CustomUser.objects.get(id=old_token["user_id"])
            # Create new tokens
            new_refresh_token = RefreshToken.for_user(user)

            new_access_token = str(new_refresh_token.access_token)

            response = Response(
                {"detail": "Tokens refreshed successfully"},
                status=status.HTTP_200_OK,
            )

            # Set new cookies
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite="None",
            )

            response.set_cookie(
                key="refresh_token",
                value=str(new_refresh_token),
                httponly=True,
                secure=True,
                samesite="None",
            )

            return response

        # If refresh token is expired or invalid → DELETE IT
        except (InvalidToken, TokenError) as e:
            response = Response(
                {"detail": "Refresh token expired or invalid.", "error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

            response.set_cookie(
                key="access_token",
                value="",
                httponly=True,
                secure=True,
                samesite="None",
                expires="Thu, 01 Jan 1970 00:00:00 GMT",  # Expire immediately
                max_age=0,  # Zero max age
            )
            response.set_cookie(
                key="refresh_token",
                value="",
                httponly=True,
                secure=True,
                samesite="None",
                expires="Thu, 01 Jan 1970 00:00:00 GMT",  # Expire immediately
                max_age=0,  # Zero max age
            )
            return response


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = CustomUser

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()  # Get the user object
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user.set_password(serializer.validated_data.get("new_password"))
            user.save()

            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
