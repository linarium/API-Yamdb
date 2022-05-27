from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import MinLengthValidator

from .validators import (
    check_score,
    not_me_username_validation,
    check_year_validation
)
from api_yamdb.settings import CODE_LENGTH, EMAIL_LENGTH, USERNAME_LENGTH


class User(AbstractUser):

    USER_ROLE = 'user'
    MODERATOR_ROLE = 'moderator'
    ADMIN_ROLE = 'admin'

    ACCESS_ROLES = (
        (USER_ROLE, 'user'),
        (MODERATOR_ROLE, 'moderator'),
        (ADMIN_ROLE, 'admin')
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=USERNAME_LENGTH,
        unique=True,
        validators=[
            ASCIIUsernameValidator(),
            not_me_username_validation
        ]
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=EMAIL_LENGTH,
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    role = models.CharField(
        max_length=max(
            len(iteration[0]) for iteration in ACCESS_ROLES),
        choices=ACCESS_ROLES,
        default=USER_ROLE,
        blank=False,
        verbose_name='роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='досье',
        help_text='Расскажите о себе'
    )
    confirmation_code = models.CharField(
        max_length=CODE_LENGTH,
        blank=True,
        null=True,
        validators=[MinLengthValidator(CODE_LENGTH)],
        verbose_name='Код подтверждения'
    )

    @property
    def is_user(self):
        return self.role == self.USER_ROLE

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR_ROLE

    @property
    def is_admin(self):
        return (self.role == self.ADMIN_ROLE
                or self.is_staff)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user_code'
            ),
        ]


class CategoryGenre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoryGenre):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenre):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField(
        verbose_name='Название',
        help_text='Введите название произведения'
    )
    year = models.IntegerField(
        validators=[check_year_validation],
        verbose_name='Год',
        help_text='Введите дату выхода произведения'
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание',
        help_text='Добавьте описание произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
        help_text='Выберите категорию произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Выберите жанр произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class CommentReview(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        abstract = True


class Review(CommentReview):
    OBJ_STR_TEXT = 'title:{}, author:{}, score:{}, text:{:.50}...'

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    score = models.IntegerField(
        validators=[check_score],
        verbose_name='Оценка',
        help_text='Поставьте оценку произведению от 1 до 10'
    )

    class Meta(CommentReview.Meta):
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review'
            ),
            models.CheckConstraint(
                check=models.Q(score__gte=1),
                name='score_gte_1'
            ),
            models.CheckConstraint(
                check=models.Q(score__lte=10),
                name='score_lte_10'
            )
        ]

    def __str__(self):
        return self.OBJ_STR_TEXT.format(
            self.title.name,
            self.author.username,
            self.score,
            self.text
        )


class Comment(CommentReview):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta(CommentReview.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:30]
