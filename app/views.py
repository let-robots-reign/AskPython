from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from app.models import Profile, Question, Answer
from django.core.exceptions import ObjectDoesNotExist


def paginate(objects_list, request, per_page=20):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return page


def new_questions(request):
    questions = Question.objects.new_questions()
    page = paginate(questions, request, 20)
    return render(request, 'new_questions.html', {
        'page_obj': page
    })


def hot_questions(request):
    questions = Question.objects.hot_questions()
    page = paginate(questions, request, 20)
    return render(request, 'hot_questions.html', {
        'page_obj': page
    })


def question_page(request, pk):
    try:
        question = Question.objects.get(id=pk)
        answers = question.answers.best_answers()
        page = paginate(answers, request, 20)
        return render(request, 'question_page.html', {
            'question': question,
            'page_obj': page
        })
    except ObjectDoesNotExist:
        # question doesn't exist, should return 404
        return render(request, '404_not_found.html')


def tag_questions(request, tag):
    questions = Question.objects.questions_for_tag(tag).all()
    if len(questions) > 0:
        page = paginate(questions, request, 20)
        return render(request, 'questions_for_tag.html', {
            'page_obj': page,
            'tag': tag
        })
    else:
        return render(request, 'blank_page.html')


def ask_question(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')
