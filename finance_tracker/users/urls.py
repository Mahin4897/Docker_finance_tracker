from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    loginView,
    logoutView,
    CustomTokenRefreshView,
    ChangePasswordView,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", loginView.as_view(), name="login"),
    path("logout/", logoutView.as_view(), name="logout"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
