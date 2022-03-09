from rest_framework import serializers

from trainingapp.models import Topic


class TopicsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ("id", "title")


class TopicModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = '__all__'
