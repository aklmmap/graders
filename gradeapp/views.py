from django.shortcuts import render,redirect
from .models import Exam, Question
from django.contrib import messages
from django.http import HttpResponse
import csv

import joblib
import pandas as pd
import numpy as np

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
    return rounded_score


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
    exams = Exam.objects.all()
    return render(request, 'exam_list.html', {'exams': exams})

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
            messages.success(request, "Exam created successfully.")
            return redirect('exam_list')  # Redirect to exam list page after creating exam
    else:
        questions = Question.objects.all()
        return render(request, 'question_list.html', {'questions': questions})



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
