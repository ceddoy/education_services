from django.db import models


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
    answer = models.ManyToManyField('Answer', blank=True, verbose_name='Варианты ответов', related_name='answers_question')

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f'Вопрос №{self.id}'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', related_name='question_answers')
    answer_text = models.CharField(max_length=128, verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.answer_text
