from rest_framework.generics import ListAPIView, RetrieveAPIView

from trainingapp.models import Topic
from trainingapp.serializer import TopicsModelSerializer, TopicModelSerializer


class TopicsListView(ListAPIView):
    serializer_class = TopicsModelSerializer
    queryset = Topic.objects.all()


class TopicListView(RetrieveAPIView):
    serializer_class = TopicModelSerializer
    queryset = Topic.objects.all()
