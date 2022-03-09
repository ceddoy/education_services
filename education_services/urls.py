from django.contrib import admin
from django.urls import path

from trainingapp.views import TopicListView
from userapp.custom_auth_token import obtain_auth_token
from userapp.views import CreateUserAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clients/create/', CreateUserAPIView.as_view()),
    path('api_auth_token/', obtain_auth_token),
    path('api/topics/', TopicListView.as_view()),
    path('api/topics/<int:pk>/', TopicListView.as_view()),
]
