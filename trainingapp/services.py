from trainingapp.models import Question, ResultAnswers


def get_correct_answers(question):
    answers = question.answers.filter(is_correct=True).values('id', 'answer_text')
    return [{"id": answer.get('id'), "answer_text": answer.get('answer_text')} for answer in answers]


def result_response(request, **kwargs):
    question = Question.objects.filter(id=kwargs.get('pk')).select_related('topic').first()
    correct_answers = get_correct_answers(question)
    object_result, created = ResultAnswers.objects.get_or_create(user=request.user, topic=question.topic)
    if sorted(request.data.get("id")) == sorted([answer.get('id') for answer in correct_answers]):
        object_result.count_correct_answer()
        if question.topic.question_set.all().count() <= object_result.quantity_answers():
            return {"result": 'Правильно, тест окончен',
                    "result_answers": {"correct": object_result.count_right_answers,
                                       "wrong": object_result.count_wrong_answers}}
        return {"result": 'Правильно'}
    else:
        object_result.count_wrong_answer()
        if question.topic.question_set.all().count() <= object_result.quantity_answers():
            return {"result": 'Неправильно, тест окончен',
                    "result_answers": {"correct": object_result.count_right_answers,
                                       "wrong": object_result.count_wrong_answers}}
        return {"result": 'Неправильно', "correct_answer": correct_answers}
