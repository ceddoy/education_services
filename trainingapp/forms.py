from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class QuestionAnswersFormSet(BaseInlineFormSet):
    def clean(self) -> dict:
        super().clean()
        for answer in self.cleaned_data:
            if answer.get('answer').is_correct:
                return self.cleaned_data
        raise ValidationError('Необходимо создать хотя бы 1 правильный ответ')
