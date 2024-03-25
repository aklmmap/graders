from django.contrib import admin

from .models import Student,User,Exam,Teacher,Question


# Register your models here.

admin.site.register(Exam)
admin.site.register(Student)
admin.site.register(Teacher)

admin.site.register(User)

#admin.site.register(Question)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
   list_display=['question_text']
