from django.contrib import admin
from django.urls import path

from trainingapp.views import TopicRetrieveAPIView, TopicsListView, QuestionRetrieveAPIView
from userapp.custom_auth_token import obtain_auth_token
from userapp.views import CreateUserAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clients/create/', CreateUserAPIView.as_view(), name='create_user'),
    path('api_auth_token/', obtain_auth_token, name='get_token'),
    path('api/topics/', TopicsListView.as_view(), name='topics'),
    path('api/topics/<int:pk>/', TopicRetrieveAPIView.as_view(), name='topic_detail'),
    path('api/test/<int:pk>/', QuestionRetrieveAPIView.as_view(), name='question'),
]
