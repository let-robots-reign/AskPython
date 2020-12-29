from app.models import Profile, Tag


def best_profiles(request):
    return {'best_profiles': Profile.objects.get_best_profiles()}


def best_tags(request):
    return {'best_tags': Tag.objects.get_best_tags()}
