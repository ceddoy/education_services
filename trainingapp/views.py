from django.db.models import Q
from django.http import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView

from trainingapp.models import Topic, Question, Answer
from trainingapp.serializer import TopicsModelSerializer, TopicModelSerializer, QuestionModelSerializer


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
        answer_correct = sorted([answer_id.id for answer_id in Answer.objects.filter(Q(question_id=kwargs.get('pk')) &
                                                                      Q(is_correct=True))])
        input_user = [answer_id.split(',') for answer_id in dict(request.data).get('id')]
        input_answer = sorted(list(map(int, input_user[0])))
        if answer_correct == input_answer:
            return JsonResponse({"result": 'Правильно'})
        else:
            return JsonResponse({"result": 'Не правильно', "correct_answer": answer_correct})
