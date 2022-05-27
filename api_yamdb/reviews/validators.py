import datetime as dt

from rest_framework.exceptions import ValidationError


def not_me_username_validation(value):
    if value == 'me':
        raise ValidationError(
            'Нельзя использовать "me" в качестве имени пользователя.')


def check_year_validation(value):
    if value > dt.date.today().year:
        raise ValidationError(
            f'Неверное указание года. {value} год ещё не наступил.')


def check_score(value):
    if not 1 <= value <= 10:
        raise ValidationError(
            f'Вы пытаетесь поставить оценку {value}. '
            'Поставтьте оценку от 1 до 10 включительно.')
