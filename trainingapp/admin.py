from django.contrib import admin

from trainingapp.models import Topic, Question, Answer


class AnswerViewAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_text', 'is_correct')
    search_fields = ('question__id', 'question__topic__title')
    raw_id_fields = ('question',)


class QuestionViewAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('question__id', 'question__topic__title')
    raw_id_fields = ('topic',)


class TopicViewAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('title',)


admin.site.register(Topic, TopicViewAdmin)
admin.site.register(Question, QuestionViewAdmin)
admin.site.register(Answer, AnswerViewAdmin)
