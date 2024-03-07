from django.shortcuts import render
from django.http import HttpResponse

import joblib
import pandas as pd
import numpy as np

# Load the trained model
model = joblib.load("A:/Amith/University of Windsor/Winter 2024/xgboost_model.pkl")

# Load the TF-IDF vectorizer used during training
tfidf_vectorizer = joblib.load("A:/Amith/University of Windsor/Winter 2024/tfidf_vectorizer.pkl")


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
