from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=30, verbose_name='Имя пользователя')
    profile_pic = models.ImageField(upload_to='uploads/avatars', verbose_name='Аватар')

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Tag(models.Model):
    tag_name = models.CharField(primary_key=True, max_length=30, verbose_name='Название тега')

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by("-creation_date")

    def hot_questions(self):
        # "горячими" вопросами назовем вопросы за последние 2 дня с наивысшим рейтингом
        return self.filter(creation_date__gte=(timezone.now() - timezone.timedelta(days=1))).order_by("-rating")
        #self.filter(creation_date__lte=(timezone.now() - timezone.timedelta(days=1))).order_by("-rating")

    def questions_for_tag(self, tag):
        return self.filter(tags__tag_name=tag)


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='Заголовок вопроса')
    content = models.TextField(verbose_name='Текст вопроса')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг вопроса')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Дата создания вопроса')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', related_name='questions', related_query_name='question')
    # TODO: liked users

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_answers_count(self):
        return self.answers.count()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerManager(models.Manager):
    def best_answers(self):
        return self.order_by("-rating")


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers",
                                         related_query_name="answer")
    content = models.TextField(verbose_name='Текст ответа')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг ответа')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Дата создания ответа')
    is_marked_correct = models.BooleanField(default=False, verbose_name='Отмечен ли как верный')
    # TODO: liked users

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
