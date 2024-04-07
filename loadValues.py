import os
import django
import csv
from gradeapp.models import Question

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
django.setup()

def load_questions_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Assuming your CSV file has a column named 'question_text'
            question_text = row['question_text']

            # Create a new Question instance and save it
            question = Question.objects.create(question_text=question_text)
            # You can add other fields here if needed

            print(f"Question '{question_text}' created.")


if __name__ == "__main__":
    csv_file_path = "D:/Masters Classes/Sem 4/graders/Questions.csv"
    load_questions_from_csv(csv_file_path)