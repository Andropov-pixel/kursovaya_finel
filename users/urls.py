from django.urls import path

from .serializers import MyTokenObtainPairSerializer
from .views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "token/",
        TokenObtainPairView.as_view(serializer_class=MyTokenObtainPairSerializer),
        name="token_obtain_pair",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
