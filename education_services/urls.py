from django.contrib import admin
from django.urls import path

from userapp.custom_auth_token import obtain_auth_token
from userapp.views import CreateUserAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clients/create/', CreateUserAPIView.as_view()),
    path('api_auth_token/', obtain_auth_token),
]
