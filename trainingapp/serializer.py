from rest_framework import serializers

from trainingapp.models import Topic, Answer, Question


class TopicsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ("id", "title")


class TopicModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = '__all__'


class AnswersForQuestionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'answer_text',)


class QuestionModelSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField('get_answers_for_question')

    @staticmethod
    def get_answers_for_question(obj):
        answers_list = Answer.objects.filter(question=obj.pk)
        serializer = AnswersForQuestionModelSerializer(answers_list, many=True)
        return serializer.data

    class Meta:
        model = Question
        fields = ('question_text', 'answers')
