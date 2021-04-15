from app.models import Profile, Tag
from django.core.cache import cache


def best_profiles(request):
    best = cache.get('best_profiles')
    return {'best_profiles': best}


def best_tags(request):
    best = cache.get('best_tags')
    return {'best_tags': best}
