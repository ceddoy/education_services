from django.http import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from trainingapp.models import Topic, Question, ResultAnswers
from trainingapp.serializer import TopicsModelSerializer, TopicModelSerializer, QuestionModelSerializer
from trainingapp.services import result_response, check_user_for_retesting, create_list_questions


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
        object_result_answers = check_user_for_retesting(request, instance)
        if object_result_answers:
            if not len(object_result_answers.list_questions):
                return JsonResponse({"error": 'По данной теме, вы уже прошли тест!'})
        elif not object_result_answers:
            self.create_object_result_answers(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create_object_result_answers(self, question):
        ResultAnswers.objects.create(user=self.request.user, topic=question.topic,
                                     list_questions=create_list_questions(question.topic))

    def post(self, request, *args, **kwargs):
        return JsonResponse(result_response(request, **kwargs))
