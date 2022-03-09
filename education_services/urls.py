from django.contrib import admin
from django.urls import path

from userapp.views import CreateUserAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clients/create/', CreateUserAPIView.as_view()),
]
