from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware

from app.models import *

from random import choice, sample, randint
from faker import Faker
from datetime import datetime

fake = Faker(["ru_RU"])


class Command(BaseCommand):
    help = 'Генерация базы данных'

    def add_arguments(self, parser):
        parser.add_argument("--profiles", type=int, help="Количество профилей")
        parser.add_argument("--questions", type=int, help="Количество вопросов")
        parser.add_argument("--answers", type=int, help="Количество ответов к вопросу")
        parser.add_argument("--tags", type=int, help="Количество тегов")
        parser.add_argument("--votes", type=int, help="Количество оценок к вопросу")

    def handle(self, *args, **kwargs):
        try:
            profiles_count = kwargs["profiles"]
            questions_count = kwargs["questions"]
            answers_per_question_count = kwargs["answers"]
            tags_count = kwargs["tags"]
            votes_per_question_number = kwargs["votes"]
        except:
            raise CommandError("Some arguments were not provided")

        self.generate_profiles(profiles_count)
        self.generate_tags(tags_count)
        self.generate_questions(questions_count)
        self.generate_answers(answers_per_question_count)
        self.generate_votes(votes_per_question_number)

    def generate_users(self, count):
        for i in range(count):
            User.objects.create_user(fake.first_name(), fake.email(),
                                     fake.password(length=fake.random_int(min=8, max=15)))

    def generate_profiles(self, count):
        self.generate_users(count)
        users_ids = list(User.objects.values_list("id", flat=True))
        profile_pics = ["avatars/profile_pic.jpeg"]

        for i in range(count):
            Profile.objects.create(user_id=users_ids[i], user_name=fake.last_name(),
                                   profile_pic=choice(profile_pics))

    def generate_tags(self, count):
        for i in range(count):
            Tag.objects.create(tag_name=fake.word())

    def generate_questions(self, count):
        profiles = list(Profile.objects.values_list("id", flat=True))

        tags = list(Tag.objects.values_list('tag_name', flat=True))

        for i in range(count):
            question = Question.objects.create(
                author_id=choice(profiles),
                title=fake.sentence(nb_words=3),
                content=fake.text(),
                creation_date=fake.date_time_between(make_aware(datetime(year=2019, month=1, day=1),
                                                                timezone.get_current_timezone()),
                                                     timezone.now())
            )

            question.tags.set(sample(tags, randint(1, len(tags))))

    def generate_answers(self, count):
        pass

    def generate_votes(self, count):
        pass
