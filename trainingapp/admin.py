from django.contrib import admin

from trainingapp.models import Topic, Question, Answer


class AnswersInLine(admin.TabularInline):
    extra = 1
    model = Question.answer.through
    readonly_fields = ('is_correct_answer',)

    def is_correct_answer(self, instance):
        return instance.answer.is_correct
    is_correct_answer.short_description = 'Правильный ответ'


class AnswerViewAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_text', 'is_correct')
    search_fields = ('question__id', 'question__topic__title')
    raw_id_fields = ('question',)


class QuestionViewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'topic')
    search_fields = ('question__id', 'question__topic__title')
    raw_id_fields = ('topic',)
    inlines = (AnswersInLine,)
    fields = ('topic', 'question_text')


class TopicViewAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('title',)


admin.site.register(Topic, TopicViewAdmin)
admin.site.register(Question, QuestionViewAdmin)
admin.site.register(Answer, AnswerViewAdmin)
