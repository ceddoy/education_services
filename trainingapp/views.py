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
        question = Question.objects.filter(id=kwargs.get('pk')).first()
        answers = question.answer.filter(is_correct=True).values('id', 'answer_text')
        correct_answers = [{"id": answer.get('id'), "answer_text": answer.get('answer_text')} for answer in answers]
        if sorted(request.data.get("id")) == sorted([answer.get('id') for answer in correct_answers]):
            return JsonResponse({"result": 'Правильно'})
        else:
            return JsonResponse({"result": 'Не правильно', "correct_answer": correct_answers})
