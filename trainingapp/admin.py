from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from trainingapp.forms import QuestionAnswersFormSet
from trainingapp.models import Topic, Question, Answer, ResultAnswers


class AnswersInLine(admin.TabularInline):
    extra = 1
    model = Question.answers.through
    formset = QuestionAnswersFormSet
    readonly_fields = ('is_correct_answer',)

    def is_correct_answer(self, instance):
        return instance.answer.is_correct
    is_correct_answer.short_description = 'Правильный ответ'


@admin.register(Answer)
class AnswerViewAdmin(admin.ModelAdmin):
    list_display = ('answer_text', 'is_correct')
    search_fields = ('answer_text',)


@admin.register(Question)
class QuestionViewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'topic', 'question_text')
    fields = ('topic', 'question_text')
    search_fields = ('topic__title',)
    raw_id_fields = ('topic',)
    inlines = (AnswersInLine,)


@admin.register(Topic)
class TopicViewAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('title',)


class ResultAnswersInLine(admin.TabularInline):
    extra = 0
    model = ResultAnswers
    readonly_fields = ('objects_result_answers_link', 'topic', 'count_right_answers',
                       'count_wrong_answers', 'created_at', 'updated_at',)

    fields = ('objects_result_answers_link', 'topic', 'count_right_answers',
              'count_wrong_answers', 'created_at', 'updated_at')

    list_display_links = ("__str__", "topic")

    def objects_result_answers_link(self, obj):
        url = reverse("admin:trainingapp_resultanswers_change", args=(obj.id,))
        return mark_safe(f'<a href="{url}">{obj.id}</a>')
    verbose_name = 'История прохождения тестов'
    objects_result_answers_link.short_description = 'ID результатов тестирования'


@admin.register(ResultAnswers)
class ResultAnswersViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'created_at', 'updated_at')
    search_fields = ('id', 'user__email', 'topic__title')
    raw_id_fields = ('user', 'topic')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'topic')
