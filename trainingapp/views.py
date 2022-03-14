from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from education_services.yasg import response_schema_answer_question, response_schema_topics_detail, \
    request_body_answer_question
from trainingapp.models import Topic, Question, ResultAnswers
from trainingapp.serializer import TopicsModelSerializer, TopicModelSerializer, QuestionModelSerializer
from trainingapp.services import result_answer_question, check_user_for_retesting, create_list_questions


class TopicsListView(ListAPIView):
    serializer_class = TopicsModelSerializer
    queryset = Topic.objects.all()


class TopicRetrieveAPIView(RetrieveAPIView):
    serializer_class = TopicModelSerializer
    queryset = Topic.objects.all()

    @swagger_auto_schema(responses=response_schema_topics_detail)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class QuestionRetrieveAPIView(RetrieveAPIView):
    serializer_class = QuestionModelSerializer
    queryset = Question.objects.all()
    http_method_names = ['get', 'post']

    def retrieve(self, request, *args, **kwargs) -> Response or JsonResponse:
        instance = self.get_object()
        object_result_answers = check_user_for_retesting(request, instance)
        if object_result_answers:
            if not len(object_result_answers.list_questions):
                return JsonResponse({"error": 'По данной теме, вы уже прошли тест!'})
        elif not object_result_answers:
            self.create_object_result_answers(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create_object_result_answers(self, question: Question) -> None:
        ResultAnswers.objects.create(user=self.request.user, topic=question.topic,
                                     list_questions=create_list_questions(question.topic))

    @swagger_auto_schema(request_body=request_body_answer_question, responses=response_schema_answer_question)
    def post(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(result_answer_question(request, **kwargs))
