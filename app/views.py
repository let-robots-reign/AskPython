from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, reverse

from app.models import Profile, Question, Answer
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from app.forms import LoginForm, AskForm


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


@login_required
def ask_question(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.profile
            question.save()
            question.tags.set(form.cleaned_data['tags'])
            return redirect(reverse('question_page', kwargs={'pk': question.id}))

    return render(request, 'ask.html', {'form': form})


def login(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect('/')  # TODO: правильный redirect

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')
