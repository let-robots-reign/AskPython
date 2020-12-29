from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django_resized import ResizedImageField


class ProfileManager(models.Manager):
    def get_best_profiles(self):
        # TODO: реальный запрос лучших пользователей
        return self.all()[:10]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=30, verbose_name='Ник пользователя')
    # resizing the picture to not break the html markup
    profile_pic = ResizedImageField(size=[50, 64], quality=100, upload_to='avatars/%Y/%m/%d',
                                    default='avatars/default_pic.png', verbose_name='Аватар')

    objects = ProfileManager()

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class TagManager(models.Manager):
    def get_best_tags(self):
        # TODO: реальный запрос лучших тегов
        return self.all()[:10]


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True, verbose_name='Название тега')

    objects = TagManager()

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by("-creation_date")

    def hot_questions(self):
        # "горячими" вопросами назовем вопросы с наивысшим рейтингом
        return self.order_by("-rating")

    def questions_for_tag(self, tag):
        return self.filter(tags__tag_name=tag)


class Question(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='Заголовок вопроса')
    content = models.TextField(verbose_name='Текст вопроса')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг вопроса')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания вопроса')
    tags = models.ManyToManyField('Tag', verbose_name='Теги', related_name='questions', related_query_name='question')
    # users who voted for the question
    votes = models.ManyToManyField('Profile', blank=True, verbose_name="Оценки вопроса", through='QuestionVote',
                                   related_name="voted_questions", related_query_name="voted_questions")

    objects = QuestionManager()
    current_vote = 0

    def __str__(self):
        return self.title

    def update_rating(self):
        self.rating = QuestionVote.objects.get_rating(self.id)
        self.save()

    def get_answers_count(self):
        return self.answers.count()

    def get_vote_by_user(self, user):
        try:
            return self.question_votes.get(user_id=user.id).mark
        except QuestionVote.DoesNotExist:
            return None

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerManager(models.Manager):
    def best_answers(self):
        return self.order_by("-rating")


class Answer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    related_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="answers",
                                         related_query_name="answer")
    content = models.TextField(verbose_name='Текст ответа')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг ответа')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания ответа')
    is_marked_correct = models.BooleanField(default=False, verbose_name='Отмечен ли как верный')
    # users who voted for the answer
    votes = models.ManyToManyField('Profile', blank=True, verbose_name="Оценки вопроса", through='AnswerVote',
                                   related_name="voted_answers", related_query_name="voted_answer")

    objects = AnswerManager()
    current_vote = 0

    def __str__(self):
        return self.content

    def update_rating(self):
        self.rating = AnswerVote.objects.get_rating(self.id)
        self.save()

    def get_vote_by_user(self, user):
        try:
            v = self.answer_votes.get(user_id=user.id)
            return v.mark
        except AnswerVote.DoesNotExist:
            return None

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class VoteManager(models.Manager):
    LIKE = 1
    DISLIKE = -1

    def get_likes(self, pk):
        return self.filter(related_object=pk, mark=VoteManager.LIKE).count()

    def get_dislikes(self, pk):
        return self.filter(related_object=pk, mark=VoteManager.DISLIKE).count()

    def get_rating(self, pk):
        return self.get_likes(pk) - self.get_dislikes(pk)


class QuestionVote(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Кто оценил')
    mark = models.IntegerField(default=0,
                               verbose_name='Поставленная оценка')  # can be -1 = downvoted, 1 = upvoted
    related_object = models.ForeignKey('Question', related_name='question_votes',
                                       verbose_name='Оцениваемый вопрос', on_delete=models.CASCADE)

    objects = VoteManager()

    def __str__(self):
        return f'Оценка вопроса: {self.mark}'

    class Meta:
        verbose_name = 'Оценка вопроса'
        verbose_name_plural = 'Оценки вопросов'


class AnswerVote(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Кто оценил')
    mark = models.IntegerField(default=0,
                               verbose_name='Поставленная оценка')  # can be -1 = downvoted, 1 = upvoted
    related_object = models.ForeignKey('Answer', related_name='answer_votes',
                                       verbose_name='Оцениваемый ответ', on_delete=models.CASCADE)

    objects = VoteManager()

    def __str__(self):
        return f'Оценка ответа: {self.mark}'

    class Meta:
        verbose_name = 'Оценка ответа'
        verbose_name_plural = 'Оценки ответов'
