from django.contrib import admin
from tasks.models import Task, TaskAssignment


admin.site.register(Task)
admin.site.register(TaskAssignment) 