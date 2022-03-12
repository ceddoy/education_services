from django.http import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView

from trainingapp.models import Topic, Question
from trainingapp.serializer import TopicsModelSerializer, TopicModelSerializer, QuestionModelSerializer
from trainingapp.services import result_response


class TopicsListView(ListAPIView):
    serializer_class = TopicsModelSerializer
    queryset = Topic.objects.all()


class TopicRetrieveAPIView(RetrieveAPIView):
    serializer_class = TopicModelSerializer
    queryset = Topic.objects.all()


class QuestionRetrieveAPIView(RetrieveAPIView):
    serializer_class = QuestionModelSerializer
    queryset = Question.objects.all()

    def post(self, request, *args, **kwargs):
        return JsonResponse(result_response(request, **kwargs))
