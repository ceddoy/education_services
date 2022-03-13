import random

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from trainingapp.models import Question, ResultAnswers


def get_correct_answers(question):
    answers = question.answers.filter(is_correct=True).values('id', 'answer_text')
    return [{"id": answer.get('id'), "answer_text": answer.get('answer_text')} for answer in answers]


def result_answer_question(request, **kwargs):
    question = Question.objects.filter(id=kwargs.get('pk')).select_related('topic').first()
    correct_answers = get_correct_answers(question)
    object_result_answers = check_user_for_retesting(request, question)
    url = update_and_get_list_questions(object_result_answers, kwargs.get('pk'))
    if object_result_answers.list_questions:
        url = get_next_page(random.choice(object_result_answers.list_questions))
    if sorted(request.data.get("id")) == sorted([answer.get('id') for answer in correct_answers]):
        object_result_answers.count_correct_answer()
        if not object_result_answers.list_questions:
            return {"result": 'Правильно, тест окончен',
                    "result_answers": {"correct": object_result_answers.count_right_answers,
                                       "wrong": object_result_answers.count_wrong_answers}}
        return {"result": 'Правильно',
                'next_question': url}
    else:
        object_result_answers.count_wrong_answer()
        if not object_result_answers.list_questions:
            return {"result": 'Неправильно, тест окончен',
                    "correct_answer": correct_answers,
                    "result_answers": {"correct": object_result_answers.count_right_answers,
                                       "wrong": object_result_answers.count_wrong_answers}}
        return {"result": 'Неправильно', "correct_answer": correct_answers, 'next_question': url}


def create_list_questions(topic):
    return [quest.id for quest in topic.question_set.all()]


def get_next_page(question_id):
    return reverse('question', args=[question_id])


def check_user_for_retesting(request, question):
    return ResultAnswers.objects.filter(Q(user=request.user) & Q(topic=question.topic)).first()


def update_and_get_list_questions(object_result_answers, question_id):
    try:
        object_result_answers.list_questions.remove(question_id)
        object_result_answers.save(update_fields=['list_questions'])
        if object_result_answers.list_questions:
            return get_next_page(random.choice(object_result_answers.list_questions))
        return None
    except ValueError:
        raise ValidationError({"error": 'По данной теме, вы уже прошли тест!'})
