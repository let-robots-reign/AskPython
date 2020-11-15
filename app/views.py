from django.shortcuts import render

questions = [
    {'id': _ + 1,
     'title': 'Question\'s title!',
     'description': 'Description of a question',
     'num_of_answers': 3,
     'range_of_answers': range(3),
     'num_of_likes': 0,
     'tags': ['django', 'pip']}
    for _ in range(10)
]


def new_questions(request):
    return render(request, 'new_questions.html', {
        'questions': questions
    })


def hot_questions(request):
    return render(request, 'hot_questions.html', {
        'questions': questions
    })


def question_page(request, pk):
    question = questions[pk - 1]
    return render(request, 'question_page.html', {
        'question': question
    })


def ask_question(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')
