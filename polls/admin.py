from django.contrib import admin
from .models import Poll, Question, Choice, CustomUser, Class, ClassStudent, Teaching, StudentResponse, StudentQuizResult

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(CustomUser)
admin.site.register(Class)
admin.site.register(ClassStudent)
admin.site.register(Teaching)
admin.site.register(StudentResponse)
admin.site.register(StudentQuizResult)