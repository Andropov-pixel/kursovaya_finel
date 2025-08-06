from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PublicHabitListView, UserRegisterView

# Описание маршрутизации для User

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),  # Регистрация пользователя
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),  # Авторизация пользователя
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("public_list/", PublicHabitListView.as_view(), name="habits_list"),
]