from django.contrib import admin

#from .models import Student, User, Exam, Teacher, Question, ScoreSheet, Profile

from .models import Exam, Question, ScoreSheet, Person

# Register your models here.

admin.site.register(Exam)

#admin.site.register(Student)
#admin.site.register(Teacher)

#admin.site.register(User)
admin.site.register(ScoreSheet)
admin.site.register(Person)
admin.site.register(Question)

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#    list_display=['question_text']
