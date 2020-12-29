from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache

from app.models import Profile, Tag


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        best_profiles = Profile.objects.get_best_profiles()
        cache.set('best_profiles', best_profiles, 86400 + 3600)

        best_tags = Tag.objects.get_best_tags()
        cache.set('best_tags', best_tags, 86400 + 3600)
