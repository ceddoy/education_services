from django.http import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from trainingapp.models import Topic, Question
from trainingapp.serializer import TopicsModelSerializer, TopicModelSerializer, QuestionModelSerializer
from trainingapp.services import result_response, check_user_for_retesting


class TopicsListView(ListAPIView):
    serializer_class = TopicsModelSerializer
    queryset = Topic.objects.all()


class TopicRetrieveAPIView(RetrieveAPIView):
    serializer_class = TopicModelSerializer
    queryset = Topic.objects.all()


class QuestionRetrieveAPIView(RetrieveAPIView):
    serializer_class = QuestionModelSerializer
    queryset = Question.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if check_user_for_retesting(request, instance):
            return JsonResponse({"error": 'По данной теме, вы уже прошли тест!'})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return JsonResponse(result_response(request, **kwargs))
