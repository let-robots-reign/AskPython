"""AskPython URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('new/', views.new_questions, name='new_questions'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('question/<int:pk>/', views.question_page, name='question_page'),
    path('ask/', views.ask_question, name='ask_question'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('/tag/<str:tag>', views.tag_questions, name='tag_questions'),
    path('', views.new_questions, name='root'),
]
