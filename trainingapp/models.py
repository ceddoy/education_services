from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import F

from userapp.models import User


class Topic(models.Model):
    """Модель для создания тем"""

    title = models.CharField(max_length=128, verbose_name='Заголовок темы')
    description = models.TextField(verbose_name='Описание темы')

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    def __str__(self):
        return self.title


class Question(models.Model):
    """Модель для создания вопросов"""

    question_text = models.TextField(verbose_name='Текст вопроса')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='Тема вопроса')
    answers = models.ManyToManyField('Answer', blank=True, verbose_name='Варианты ответов', related_name='answers_question')

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f'Вопрос №{self.id}'


class Answer(models.Model):
    answer_text = models.CharField(max_length=128, verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.answer_text


class ResultAnswers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='Тема')
    count_right_answers = models.PositiveSmallIntegerField(default=0, verbose_name='Количество верных ответов')
    count_wrong_answers = models.PositiveSmallIntegerField(default=0, verbose_name='Количество неверных ответов')
    list_questions = ArrayField(models.PositiveIntegerField(), verbose_name='Список id вопросов')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')

    class Meta:
        verbose_name = "Результат тестирования"
        verbose_name_plural = "Результаты тестирования"

    def count_correct_answer(self):
        self.count_right_answers = F('count_right_answers') + 1
        self.save(update_fields=['count_right_answers'])
        self.refresh_from_db()

    def count_wrong_answer(self):
        self.count_wrong_answers = F('count_wrong_answers') + 1
        self.save(update_fields=['count_wrong_answers'])
        self.refresh_from_db()

    def quantity_answers(self):
        return self.count_right_answers + self.count_wrong_answers
