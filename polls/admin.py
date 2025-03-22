from django.contrib import admin
from .models import Poll, Question, Choice, Response, CustomUser, Class, ClassStudent, Teaching

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Response)
admin.site.register(CustomUser)
admin.site.register(Class)
admin.site.register(ClassStudent)
admin.site.register(Teaching)