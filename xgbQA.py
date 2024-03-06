import joblib
import pandas as pd
import numpy as np

# Load the trained model
model = joblib.load("xgboost_model.pkl")

# Load the TF-IDF vectorizer used during training
tfidf_vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Function to preprocess user input and predict score
def predict_score(question, answer):
    # Transform user input using the pre-fit TF-IDF vectorizer
    X_input = tfidf_vectorizer.transform([question + ' ' + answer])
    
    # Predict score
    score = model.predict(X_input)
    rounded_score = np.round(score*2)/2
    return rounded_score
    
while 1:
    
# Take user input
    question = input("Enter the question: ")
    answer = input("Enter the answer: ")

# Predict the score
    predicted_score = predict_score(question, answer)

    print("Predicted Score:", predicted_score)
    
