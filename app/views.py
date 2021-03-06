from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, reverse
from django.db import transaction

from app.models import *
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings as app_settings
from app.forms import *

import jwt
from cent import Client
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


def add_vote_to_object(question_or_answer, user):
    if user.is_authenticated:
        question_or_answer.current_vote = question_or_answer.get_vote_by_user(user)
    else:
        question_or_answer.current_vote = None
    return question_or_answer


def new_questions(request):
    questions = Question.objects.new_questions()
    questions = [add_vote_to_object(question, request.user) for question in questions]
    page = paginate(questions, request, 20)
    return render(request, 'new_questions.html', {
        'page_obj': page
    })


def hot_questions(request):
    questions = Question.objects.hot_questions()
    questions = [add_vote_to_object(question, request.user) for question in questions]
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
    answers = [add_vote_to_object(answer, request.user) for answer in answers]
    page = paginate(answers, request, 20)
    if not request.user.is_authenticated:
        # showing page without answer form
        return render(request, 'question_page.html', {
            'question': add_vote_to_object(question, request.user),
            'page_obj': page
        })

    # формируем token для фронтенда
    channel_id = str(question.id)
    token = jwt.encode({"sub": channel_id}, app_settings.CENTRIFUGO_SECRET_KEY)

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

            client = Client('http://127.0.0.1:8000', api_key=app_settings.CENTRIFUGO_API_KEY, timeout=1)
            client.publish('new_answer', {})

            return response

    return render(request, 'question_page.html', {
        'question': add_vote_to_object(question, request.user),
        'page_obj': page,
        'form': form,
        'jwt_token': token
    })


def tag_questions(request, tag):
    questions = Question.objects.questions_for_tag(tag).all()
    questions = [add_vote_to_object(question, request.user) for question in questions]
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
    if request.user.is_authenticated:
        return HttpResponseForbidden("You already signed up")
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


@require_POST
def vote(request):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': request.build_absolute_uri(app_settings.LOGIN_URL)})

    def check_existing_vote(obj_type, user_id, obj_id):
        if obj_type == 'question':
            try:
                existing_vote = QuestionVote.objects.get(
                    user_id=user_id,
                    related_object_id=obj_id
                )
            except QuestionVote.DoesNotExist:
                existing_vote = None
        else:
            try:
                existing_vote = AnswerVote.objects.get(
                    user_id=user_id,
                    related_object_id=obj_id
                )
            except AnswerVote.DoesNotExist:
                existing_vote = None

        return existing_vote

    def create_vote_for_object(obj_type, user_id, obj_id, mark):
        # TODO: make global
        client = Client('http://127.0.0.1:8000', api_key=app_settings.CENTRIFUGO_API_KEY, timeout=1)

        if obj_type == 'question':
            # TODO: current rating instead of mark!
            client.publish('question_vote', {
                'user_id': user_id,
                'question_id': obj_id,
                'mark': mark
            })
            return QuestionVote.objects.create(
                user_id=user_id,
                related_object_id=obj_id,
                mark=mark
            )
        else:
            # TODO: ограничить канал
            client.publish('answers_vote', {
                'user_id': user_id,
                'answer_id': obj_id,
                'mark': mark
            })
            return AnswerVote.objects.create(
                user_id=user_id,
                related_object_id=obj_id,
                mark=mark
            )

    data = request.POST

    object_type = data['object_type']
    action = data['action']
    object_id = data['id']
    # проверяем, есть ли уже оценка
    existing = check_existing_vote(object_type, request.user.id, object_id)
    if existing:
        # уже была оценка
        existing.delete()  # удаляем существующую оценку
        if existing.mark == VoteManager.LIKE:
            # меняем оценку на дизлайк
            if action == 'downvote':
                create_vote_for_object(object_type, request.user.id, object_id, VoteManager.DISLIKE)
        else:
            # меняем оценку на лайк
            if action == 'upvote':
                create_vote_for_object(object_type, request.user.id, object_id, VoteManager.LIKE)
    else:
        mark = VoteManager.LIKE if action == 'upvote' else VoteManager.DISLIKE
        create_vote_for_object(object_type, request.user.id, object_id, mark)

    if object_type == 'question':
        question = Question.objects.get(id=object_id)
        question.update_rating()
    else:
        answer = Answer.objects.get(id=object_id)
        answer.update_rating()

    return JsonResponse({'status': 'success'})


@require_POST
def mark_correct(request):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': request.build_absolute_uri(app_settings.LOGIN_URL)})

    data = request.POST
    question_id = data['qid']
    answer_id = data['ansid']
    if request.user != Question.objects.get(id=question_id).author.user:
        return JsonResponse({'error': 'Вы не являетесь автором вопроса'})

    # ответ, который пользователь хочет отметить
    answer = Answer.objects.get(id=answer_id)
    # проверяем, что нет уже отмеченных
    if any(ans.is_marked_correct and ans != answer for ans in Question.objects.get(id=question_id).answers.all()):
        return JsonResponse({'error': 'Вы уже отмечали правильным другой ответ'})

    answer.is_marked_correct = not answer.is_marked_correct
    answer.save()
    return JsonResponse({'status': 'success'})


def print_parameters(request):
    if request.GET:
        html = f"<html><body>GET: {dict(request.GET)}</body></html>"
    elif request.POST:
        html = f"<html><body>POST: {dict(request.POST)}</body></html>"
    else:
        html = f"<html><body>No params!</body></html>"
    return HttpResponse(html)
