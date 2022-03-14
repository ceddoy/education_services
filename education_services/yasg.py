from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Education Services",
        default_version='v1',
        description="Test description",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

request_body_answer_question = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_ARRAY,
                                 items=openapi.TYPE_INTEGER,
                                 description='int, int')
        })

response_schema_answer_question = {
    "2001": openapi.Response(
        description="(click Example Value) 200 response,если пользователь ответил неправильно, но тест еще не окончен",
        examples={
            "application/json": {
                "result": "Неправильно",
                "correct_answer": [
                    {
                        "id": 0,
                        "answer_text": "string"
                    }
                ],
                "next_question": "url"
            },
        }
    ),
    "2002": openapi.Response(
        description="(click Example Value) 200 response,если пользователь ответил правильно, но тест еще не окончен",
        examples={
            "application/json": {
                "result": "Правильно",
                "next_question": "url"
            },
        }
    ),
    "2003": openapi.Response(
        description="(click Example Value) 200 response,если пользователь ответил неправильно на последний вопрос",
        examples={
            "application/json": {
                "result": "Неправильно, тест окончен",
                "correct_answer": [
                    {
                        "id": 0,
                        "answer_text": "string"
                    }
                ],
                "result_answers": {
                    "correct": 1,
                    "wrong": 1
                }
            },
        }
    ),
    "2004": openapi.Response(
        description="(click Example Value) 200 response, если пользователь ответил правильно на последний вопрос",
        examples={
            "application/json": {
                "result": "Правильно, тест окончен",
                "result_answers": {
                    "correct": 1,
                    "wrong": 1
                }
            },
        }
    )
}

response_schema_topics_detail = {
    "200": openapi.Response(
        description='click Example Value',
        examples={
            "application/json": {
                "id": 0,
                "title": "string",
                "description": "string",
                "start_testing_url": "url"
            }
        }
    )
}
