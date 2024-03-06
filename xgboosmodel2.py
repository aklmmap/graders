import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score,mean_absolute_error, mean_squared_error, r2_score

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


df = pd.read_csv('C:\\Users\\amith\\Downloads\\QA_dataset.csv')

df.head()

tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X = tfidf_vectorizer.fit_transform(df['question'] + ' ' + df['answer'])
y = df['score']

#y = y.apply(lambda x: 1 if x > 4 else 0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = xgb.XGBRegressor(objective='reg:squarederror')

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_pred_rounded = [round(pred * 2) / 2 for pred in y_pred]


# Print actual and predicted scores side by side
print("Actual Scores vs Predicted Scores:")
for actual, predicted in zip(y_test.values, y_pred_rounded):
    print(f"Actual: {actual}, Predicted: {predicted}")
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae:.2f}")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")
y_pred_binary = np.where(y_pred >= 4, 1, 0)
ybinary = y_test.apply(lambda x: 1 if x >= 4 else 0)
# Calculate confusion matrix
conf_matrix = confusion_matrix(ybinary, y_pred_binary)

accuracy = accuracy_score(ybinary, y_pred_binary)
accuracy_percentage = accuracy * 100
print(f"Accuracy: {accuracy_percentage:.2f}%")
print("Confusion Matrix:")
print(conf_matrix)
print("\nClassification Report:")
print(classification_report(ybinary, y_pred_binary))

joblib.dump(model,"xgboost_model.pkl");
joblib.dump(tfidf_vectorizer,"tfidf_vectorizer.pkl")




