import time

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from trainingapp.models import Topic, Question, Answer, ResultAnswers
from trainingapp.services import formation_data_for_send_email
from trainingapp.tasks import send_email_to_user_result_answers
from userapp.models import User


class TestAuthTokenMixin:
    def get_token(self) -> str:
        auth = self.client.post('/api_auth_token/', {'email': 'mail01@mail.ru', 'password': '123454321qw'})
        return f'Token {auth.data.get("token")}'


class TestTopics(APITestCase, TestAuthTokenMixin):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(email='mail01@mail.ru', password='123454321qw')
        Topic.objects.create(title='Природа', description='Природа - это природа')
        Topic.objects.create(title='Космос', description='Космос - это Космос')
        Topic.objects.create(title='История', description='История - это История')
        cls.api_topics_url = reverse("topics")

    def test_topics_view_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token())
        response = self.client.get(self.api_topics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Topic.objects.all().count())

    def test_topics_view_without_token(self):
        response = self.client.get(self.api_topics_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTopicDetail(APITestCase, TestAuthTokenMixin):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(email='mail01@mail.ru', password='123454321qw')
        topic = Topic.objects.create(title='Природа', description='Природа - это природа')
        cls.api_topic_detail_url = reverse("topic_detail", args=[topic.id])

    def test_topic_detail_view_without_token(self):
        response = self.client.get(self.api_topic_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_topic_detail_view_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token())
        response = self.client.get(self.api_topic_detail_url)
        self.assertTrue('Природа' == response.data.get("title"))
        self.assertTrue('description' in response.data.keys())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_topic_detail_view_without_questions(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token())
        response = self.client.get(self.api_topic_detail_url)
        self.assertTrue('Природа' == response.data.get("title"))
        self.assertTrue('description' in response.data.keys())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_topic_detail_view_with_questions(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token())
        response = self.client.get(self.api_topic_detail_url)
        answer_1 = Answer.objects.create(answer_text="Воздушная атмосфера", is_correct=False)
        answer_2 = Answer.objects.create(answer_text="Луна", is_correct=False)
        answer_3 = Answer.objects.create(answer_text="Планета", is_correct=True)
        question = Question.objects.create(question_text="Земля - это...",
                                           topic=Topic.objects.get(id=response.data.get('id')))
        question.answers.add(answer_1, answer_2, answer_3)

        response = self.client.get(self.api_topic_detail_url)
        self.assertTrue(Question.objects.filter(topic_id=response.data.get('id')).first() is not None)
        self.assertTrue('Природа' == response.data.get("title"))
        self.assertTrue('description' in response.data.keys())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_topic_detail_view_non_existent_topic(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token())
        response = self.client.get(reverse("topic_detail", args=[3]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestQuestions(APITestCase, TestAuthTokenMixin):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(email='mail01@mail.ru', password='123454321qw')
        topic = Topic.objects.create(title='Природа', description='Природа - это природа')
        cls.topic = topic
        answer_1_to_quest_1 = Answer.objects.create(answer_text="Воздушная атмосфера", is_correct=True)
        cls.answer_1_to_quest_1 = answer_1_to_quest_1
        answer_2_to_quest_1 = Answer.objects.create(answer_text="Луна", is_correct=False)
        cls.answer_2_to_quest_1 = answer_2_to_quest_1
        answer_3_to_quest_1 = Answer.objects.create(answer_text="Планета", is_correct=True)
        cls.answer_3_to_quest_1 = answer_3_to_quest_1
        question_1 = Question.objects.create(question_text="Земля - это...",
                                             topic=topic)
        question_1.answers.add(answer_1_to_quest_1, answer_2_to_quest_1, answer_3_to_quest_1)
        cls.question_1 = question_1

        answer_1_to_quest_2 = Answer.objects.create(answer_text="Мясоеды", is_correct=False)
        cls.answer_1_to_quest_2 = answer_1_to_quest_2
        answer_2_to_quest_2 = Answer.objects.create(answer_text="Всеядны", is_correct=True)
        cls.answer_2_to_quest_2 = answer_2_to_quest_2
        answer_3_to_quest_2 = Answer.objects.create(answer_text="Травоядны", is_correct=False)
        cls.answer_3_to_quest_2 = answer_3_to_quest_2
        answer_4_to_quest_2 = Answer.objects.create(answer_text="Очень всеядны", is_correct=True)
        cls.answer_4_to_quest_2 = answer_4_to_quest_2
        question_2 = Question.objects.create(question_text="По своему типу питания медведи ... ",
                                             topic=topic)
        question_2.answers.add(answer_1_to_quest_2, answer_2_to_quest_2, answer_3_to_quest_2, answer_4_to_quest_2)
        cls.question_2 = question_2
        cls.api_topic_detail_url = reverse("topic_detail", args=[topic.id])

    def test_url_starting_questions(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token())
        response_topic = self.client.get(self.api_topic_detail_url)
        response_question = self.client.get(response_topic.data.get("start_testing_url"))
        self.assertEqual(response_question.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_question.data.get("answers")), self.question_1.answers.all().count())

        # При переходе на начало теста, создается объект ResultAnswers
        self.assertTrue(bool(ResultAnswers.objects.filter(user=self.test_user, topic=self.topic).first()))

    def test_user_correct_wrong_to_question(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token())
        response_topic = self.client.get(self.api_topic_detail_url)
        response_question = self.client.get(response_topic.data.get("start_testing_url"))
        self.assertEqual(response_question.status_code, status.HTTP_200_OK)
        answers = {
            "id": [self.answer_2_to_quest_1.id]
        }
        response_answer_question = self.client.post(response_topic.data.get("start_testing_url"),
                                                    answers)
        self.assertEqual(response_answer_question.status_code, status.HTTP_200_OK)
        result_answers = ResultAnswers.objects.filter(user=self.test_user, topic=self.topic).first()
        self.assertTrue(result_answers.count_right_answers == 0)
        self.assertTrue(result_answers.count_wrong_answers == 1)

    def test_user_correct_answers_to_question(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token())
        response_topic = self.client.get(self.api_topic_detail_url)
        self.client.get(response_topic.data.get("start_testing_url"))
        answers_to_quest_1 = {"id": [self.answer_3_to_quest_1.id, self.answer_1_to_quest_1.id]}
        response_answer_question = self.client.post(response_topic.data.get("start_testing_url"),
                                                    answers_to_quest_1, format='json')

        self.assertEqual(response_answer_question.status_code, status.HTTP_200_OK)
        result_answers_1 = ResultAnswers.objects.filter(user=self.test_user, topic=self.topic).first()
        self.assertTrue(result_answers_1.count_right_answers == 1)
        self.assertTrue(result_answers_1.count_wrong_answers == 0)

        next_question_url = reverse('question', args=[result_answers_1.list_questions[0]])
        response_question = self.client.get(next_question_url)
        self.assertEqual(len(response_question.data.get("answers")), self.question_2.answers.all().count())
        self.assertEqual(response_question.status_code, status.HTTP_200_OK)

        answers_to_quest_2 = {"id": [self.answer_2_to_quest_2.id, self.answer_4_to_quest_2.id]}

        response_answer_question = self.client.post(next_question_url, answers_to_quest_2, format='json')
        self.assertEqual(response_answer_question.status_code, status.HTTP_200_OK)

        result_answers_2 = ResultAnswers.objects.filter(user=self.test_user, topic=self.topic).first()
        self.assertTrue(result_answers_2.count_right_answers == 2)
        self.assertTrue(result_answers_2.count_wrong_answers == 0)
        self.send_email_after_questions(result_answers_2)

    def send_email_after_questions(self, result_answers: ResultAnswers):
        result_send_email = send_email_to_user_result_answers.delay(
            formation_data_for_send_email(self.test_user, self.question_2, result_answers))
        time.sleep(3)
        self.assertTrue(result_send_email.successful())
