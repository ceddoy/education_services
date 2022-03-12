import random

from django.db.models import Q
from rest_framework.reverse import reverse

from trainingapp.models import Question, ResultAnswers


def get_correct_answers(question):
    answers = question.answers.filter(is_correct=True).values('id', 'answer_text')
    return [{"id": answer.get('id'), "answer_text": answer.get('answer_text')} for answer in answers]


def result_response(request, **kwargs):
    question = Question.objects.filter(id=kwargs.get('pk')).select_related('topic').first()
    correct_answers = get_correct_answers(question)
    object_result = ResultAnswers.objects.filter(Q(user=request.user) & Q(topic=question.topic)).first()
    if not object_result:
        object_result = ResultAnswers.objects.create(user=request.user, topic=question.topic, list_questions=create_list_questions(question.topic))
    object_result.list_questions.remove(kwargs.get('pk'))
    object_result.save(update_fields=['list_questions'])
    if object_result.list_questions:
        url = get_next_page(random.choice(object_result.list_questions))
    if sorted(request.data.get("id")) == sorted([answer.get('id') for answer in correct_answers]):
        object_result.count_correct_answer()
        if not object_result.list_questions:
            return {"result": 'Правильно, тест окончен',
                    "result_answers": {"correct": object_result.count_right_answers,
                                       "wrong": object_result.count_wrong_answers}}
        return {"result": 'Правильно',
                'next_question': url}
    else:
        object_result.count_wrong_answer()
        if not object_result.list_questions:
            return {"result": 'Неправильно, тест окончен',
                    "result_answers": {"correct": object_result.count_right_answers,
                                       "wrong": object_result.count_wrong_answers}}
        return {"result": 'Неправильно', "correct_answer": correct_answers, 'next_question': url}


def create_list_questions(topic):
    return [quest.id for quest in topic.question_set.all()]


def get_next_page(question_id):
    return reverse('question', args=[question_id])


def check_user_for_retesting(request, question):
    object_result_answers = ResultAnswers.objects.filter(Q(user=request.user) & Q(topic=question.topic)).first()
    if object_result_answers is None:
        return None
    elif len(object_result_answers.list_questions) == 0:
        return True
