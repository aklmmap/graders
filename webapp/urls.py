"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from gradeapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/', views.index, name='index'),
    path('questions/', views.question_list, name='question_list'),
    path('create_exam/', views.create_exam, name='create_exam'),
    path('exams/', views.exam_list, name='exam_list'),
    path('exam/<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('exam/<int:exam_id>/submit/', views.submit_answers, name='submit_answers'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('view_scoresheet/', views.view_scoresheet, name='view_scoresheet'),
    path('view_exams/', views.view_exams, name='view_exams'),
    path('view_students/<int:exam_id>/', views.view_students, name='view_students'),
    path('view_questions/<int:exam_id>/<int:user_id>/', views.view_questions, name='view_questions'),
    path('view-questions-answers/<int:exam_id>/<int:user_id>/', views.view_questions_answers, name='view_questions_answers'),
    path('login/', views.user_login, name='login'),
    path('student_dashboard/', views.student_exam_list, name='student_dashboard'),
]
