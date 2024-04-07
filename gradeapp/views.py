from django.shortcuts import render,redirect, get_object_or_404
from unicodedata import decimal
from django.db.models import Avg
from .models import Exam, Question, ScoreSheet #, Student
#from .models import User as User1
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
import csv
import joblib
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Load the trained model
model = joblib.load("D:/Masters Classes/Sem 4/graders/gradeapp/xgboost_model.pkl")

# Load the TF-IDF vectorizer used during training
tfidf_vectorizer = joblib.load("D:/Masters Classes/Sem 4/graders/gradeapp/tfidf_vectorizer.pkl")


# Function to preprocess user input and predict score
def predict_score(question, answer):
    # Transform user input using the pre-fit TF-IDF vectorizer
    X_input = tfidf_vectorizer.transform([question + ' ' + answer])

    # Predict score
    score = model.predict(X_input)
    rounded_score = np.round(score * 2) / 2
    return rounded_score[0]


def index(request):
    if request.method == 'POST':
        question = request.POST.get('question', '')
        answer = request.POST.get('answer', '')
        predicted_score = predict_score(question, answer)
        return render(request, 'result.html',
                      {'question': question, 'answer': answer, 'predicted_score': predicted_score})
    else:
        return render(request, 'home.html')

def exam_list(request):
    exams = Exam.objects.all().order_by('-id')  # Reversing the queryset by id
    return render(request, 'teacher_exam_list.html', {'exams': exams})

def student_exam_list(request):
    # Retrieve all exams
    exams = Exam.objects.all()

    # Get exams already taken by the student
    exams_taken = ScoreSheet.objects.filter(user=request.user).values_list('exam_id', flat=True)

    # Create a dictionary to store whether each exam has been taken by the student
    exams_taken_dict = {exam_id: True for exam_id in exams_taken}

    return render(request, 'exam_list.html', {'exams': exams, 'exams_taken_dict': exams_taken_dict})


def exam_detail(request, exam_id):
    exam = Exam.objects.get(pk=exam_id)
    return render(request, 'exam_detail.html', {'exam': exam})

def submit_answers(request, exam_id):
    if request.method == 'POST':
        exam = Exam.objects.get(pk=exam_id)
        answers = {}
        for question in exam.questions.all():
            answer = request.POST.get(f'question_{question.id}_answer')
            answers[question.id] = answer
        # Save answers to score sheet model (if created)
        # Redirect to a success page or somewhere else
    else:
        # Handle GET request
        pass

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'question_list.html', {'questions': questions})


def create_exam(request):
    if request.method == 'POST':
        exam_name = request.POST.get('exam_name')
        selected_questions = request.POST.getlist('questions')
        if not exam_name.strip():  # Check if exam name is blank or contains only whitespace
            messages.error(request, "Exam name cannot be blank.")
            # Redirect to question list page with error message
            return redirect('question_list')
        elif not selected_questions:
            messages.error(request, "Please select at least one question.")
            # Redirect to question list page with error message
            return redirect('question_list')
        else:
            exam = Exam.objects.create(exam_name=exam_name)
            exam.questions.set(selected_questions)
            #messages.success(request, "Exam created successfully.")
            messages.success(request, 'Exam successfully created.')
            return redirect('exam_list')  # Redirect to exam list page after creating exam
    else:
        questions = Question.objects.all()
        return render(request, 'question_list.html', {'questions': questions})


def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

def view_scoresheet(request):
    exams = Exam.objects.all()
    return render(request, 'view_scoresheet.html', {'exams': exams})

def view_exams(request):
    exams = Exam.objects.all()
    return render(request, 'view_exams.html', {'exams': exams})

def view_students(request, exam_id):
    exam = Exam.objects.get(pk=exam_id)

    # Get all distinct students who have taken the exam
    student_ids = ScoreSheet.objects.filter(exam_id=exam_id).values_list('user', flat=True).distinct()
    students = User.objects.filter(id__in=student_ids)

    return render(request, 'view_students.html', {'students': students, 'exam': exam})


def view_questions(request, exam_id, user_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    student = get_object_or_404(User, pk=user_id)
    questions_with_answers = ScoreSheet.objects.filter(exam_id=exam_id, user_id=user_id)
    return render(request, 'view_questions.html', {'exam': exam, 'student': student, 'questions_with_answers': questions_with_answers})

def view_questions_answers(request, exam_id, user_id):
    # Retrieve the exam object
    exam = get_object_or_404(Exam, pk=exam_id)

    # Retrieve the scoresheets for the specified exam and user
    scoresheets = ScoreSheet.objects.filter(exam_id=exam_id, user_id=user_id)

    # Calculate the total score (average of all question scores)
    total_score = scoresheets.aggregate(Avg('score'))['score__avg']

    return render(request, 'view_questions_answers.html', {'exam': exam, 'scoresheets': scoresheets, 'total_score': total_score})

def submit_answers(request, exam_id, exam=None):
    if request.method == 'POST':
        # Retrieve the exam based on the exam_id
        exam = Exam.objects.get(pk=exam_id)

        # Iterate through the submitted answers and create ScoreSheet objects
        for question in exam.questions.all():
            answer_key = f"question_{question.id}_answer"
            answer = request.POST.get(answer_key, "")
            # Validate answer if needed
            if answer.strip():  # Check if the answer is not blank
                score = float(predict_score(question.question_text, answer))
            else:
                score = 0  # Set score to 0 if the answer is blank
            score_sheet = ScoreSheet(
                user=request.user,  # Assuming the logged-in user is associated with the answers
                exam=exam,
                question=question,
                answer=answer,
                score=score
            )
            score_sheet.save()

        # Set success message
        success_message = "Exam submitted successfully."
        return redirect('view_questions_answers', exam_id=exam_id, user_id=request.user.id)

    # Handle GET request if needed
    return render(request, 'exam_detail.html', {'exam': exam})





# def read_csv_to_list(request):
#     file_path="D:\Masters Classes\Sem 4\questions.csv"
#     data_list = []
#     with open(file_path, 'r') as file:
#         csv_reader = csv.reader(file)
#         for row in csv_reader:
#             question=Question(question_text=row[0])
#             question.save()
#     return request

# Example usage

#print(csv_data_list)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.person.is_teacher:
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            # Handle invalid login credentials
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def teacher_dashboard(request):
    # Implement teacher dashboard logic
    return render(request, 'teacher_dashboard.html')

def student_dashboard(request):
    # Implement student dashboard logic
    return render(request, 'student_dashboard.html')