from django.core.management.base import BaseCommand, CommandError
#from django.utils.timezone import make_aware

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

    def generate_users(self, count):
        for i in range(count):
            User.objects.create_user(fake.unique.first_name(), fake.email(),
                                     fake.password(length=fake.random_int(min=8, max=15)))

    def generate_profiles(self, count):
        self.generate_users(count)
        users_ids = list(User.objects.values_list("id", flat=True))
        profile_pics = ["avatars/profile_pic.jpeg", "avatars/sample.jpeg"]

        for i in range(count):
            Profile.objects.create(user_id=users_ids[i], nickname=fake.last_name(),
                                   profile_pic=choice(profile_pics))

    def generate_tags(self, count):
        for i in range(count):
            Tag.objects.create(tag_name=fake.unique.word())

    def generate_questions(self, count):
        profiles = list(Profile.objects.values_list("id", flat=True))

        for i in range(count):
            question = Question.objects.create(
                author_id=choice(profiles),
                title=fake.sentence(nb_words=3),
                content=fake.text()
                # creation_date=fake.date_time_between(make_aware(datetime(year=2019, month=1, day=1),
                #                                                 timezone.get_current_timezone()),
                #                                      timezone.now())
            )

            tags_count = Tag.objects.count()
            tags = list(set([Tag.objects.get(id=randint(1, tags_count)) for _ in range(randint(1, tags_count))]))
            question.tags.set(tags)

            # TODO: enhance votes generation
            question.votes.set(sample(profiles, randint(1, len(profiles))),
                               through_defaults={"mark": VoteManager.LIKE})
            #question.votes.set(sample(profiles, randint(1, len(profiles))),
                               #through_defaults={"mark": VoteManager.DISLIKE})
            question.update_rating()


    def generate_answers(self, count):
        profiles = list(Profile.objects.values_list("id", flat=True))
        questions = list(Question.objects.values_list("id", flat=True))
        for question_id in questions:
            for i in range(count):
                answer = Answer.objects.create(
                    author_id=choice(profiles),
                    related_question_id=question_id,
                    content=fake.text()
                    # creation_date=fake.date_time_between(make_aware(datetime(year=2020, month=10, day=1),
                    #                                                 timezone.get_current_timezone()),
                    #                                      timezone.now())
                )
