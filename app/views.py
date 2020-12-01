from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, reverse
from django.db import transaction

from app.models import *
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from app.forms import *

import logging

logger = logging.getLogger(__name__)


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
    except ObjectDoesNotExist:
        # question doesn't exist, should show 404
        return render(request, '404_not_found.html')

    answers = question.answers.best_answers()
    page = paginate(answers, request, 20)
    if not request.user.is_authenticated:
        return render(request, 'question_page.html', {
            'question': question,
            'page_obj': page
        })

    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user.profile
            answer.related_question = question
            answer.save()

            response = redirect(reverse('question_page', kwargs={'pk': question.id}))
            response['Location'] += f'#ans{answer.id}'
            return response

    return render(request, 'question_page.html', {
        'question': question,
        'page_obj': page,
        'form': form
    })


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

            # пользователь может добавить и новые теги
            tags = list(set(form.cleaned_data['tags'].split()))
            # так как тегов может быть несколько, сделаем транзакцию
            with transaction.atomic():
                tags_objects = [Tag.objects.get_or_create(tag_name=tag)[0] for tag in tags]
            question.tags.set(tags_objects)

            return redirect(reverse('question_page', kwargs={'pk': question.id}))

    return render(request, 'ask.html', {'form': form})


def login(request):
    if request.method == 'GET':
        request.session['next_page'] = request.GET.get('next', '/')
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(request.session.pop('next_page', '/'))

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    if request.method == 'GET':
        request.session['next_page'] = request.GET.get('next', '/')
        form = SignupForm()
    else:
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'])

            profile = Profile.objects.create(user=user, nickname=form.cleaned_data['nickname'])
            if form.cleaned_data['profile_pic'] is not None:
                profile.profile_pic = form.cleaned_data['profile_pic']
                profile.save()

            auth.login(request, user)
            return redirect(request.session.pop('next_page', '/'))

    return render(request, 'signup.html', {'form': form})


@login_required
def settings(request):
    if request.method == 'GET':
        form = EditForm(initial={"username": request.user.username,
                                 "nickname": request.user.profile.nickname})
    else:
        form = EditForm(request.POST, request.FILES, initial={"username": request.user.username,
                                                              "nickname": request.user.profile.nickname})
        if form.is_valid():
            user = request.user
            profile = user.profile
            if 'username' in form.changed_data:
                user.username = form.cleaned_data['username']
            if 'nickname' in form.changed_data:
                profile.nickname = form.cleaned_data['nickname']
            if 'profile_pic' in form.changed_data:
                profile.profile_pic = form.cleaned_data['profile_pic']
            profile.save()
            user.save()

    return render(request, 'settings.html', {'form': form})
