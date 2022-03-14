from rest_framework import serializers

from trainingapp.models import Topic, Answer, Question
from trainingapp.services import get_next_page


class TopicsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ("id", "title")


class TopicModelSerializer(serializers.ModelSerializer):
    start_testing_url = serializers.SerializerMethodField('get_page_begin_testing')

    class Meta:
        model = Topic
        fields = ("id", "title", 'description', 'start_testing_url')

    def get_page_begin_testing(self, topic) -> dict or str:
        question = Question.objects.filter(topic=topic).first()
        if question:
            return get_next_page(question.id)
        return {'info': 'У данной темы отсутствуют вопросы!'}


class AnswersForQuestionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'answer_text',)


class QuestionModelSerializer(serializers.ModelSerializer):
    answers = AnswersForQuestionModelSerializer(many=True)

    class Meta:
        model = Question
        fields = ('question_text', 'answers')
        read_only_fields = ('question_text', 'answers')
