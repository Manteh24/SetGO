from django.contrib import admin
from accounts.models import Trainer, Trainee, FixedSession


class FixedSessionInline(admin.TabularInline):
    model = FixedSession
    extra = 1

class TraineeAdmin(admin.ModelAdmin):
    inlines = [FixedSessionInline]

admin.site.register(Trainer)
admin.site.register(Trainee, TraineeAdmin)