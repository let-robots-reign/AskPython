from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

questions = [
    {'id': _ + 1,
     'title': f'Title of a question #{_ + 1}!',
     'description': 'Description of a question',
     'num_of_answers': 3,
     'num_of_likes': 0,
     'tags': ['django', 'pip']}
    for _ in range(50)
]


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
    page = paginate(questions, request, 20)
    return render(request, 'new_questions.html', {
        'page_obj': page
    })


def hot_questions(request):
    page = paginate(questions, request, 20)
    return render(request, 'hot_questions.html', {
        'page_obj': page
    })


def question_page(request, pk):
    question = questions[pk - 1]
    answers = [{'id': _ + 1,
                'text': f'Answer #{_ + 1}\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla aliquam elementum justo, quis efficitur mauris tincidunt dignissim. Nam eleifend nunc a cursus aliquet.',
                'num_of_likes': 0}
               for _ in range(30)]
    page = paginate(answers, request, 20)
    return render(request, 'question_page.html', {
        'question': question,
        'page_obj': page
    })


def tag_questions(request, tag):
    page = paginate(questions, request, 20)
    return render(request, 'questions_for_tag.html', {
        'page_obj': page,
        'tag': tag
    })


def ask_question(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')
