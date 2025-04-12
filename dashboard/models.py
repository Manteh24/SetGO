from datetime import date, timedelta
from django.db import models
from django.db.models import Count
from accounts.models import Trainer, Trainee, FixedSession
from tasks.models import TaskAssignment
from appointments.models import AppointmentRequest
from gamification.models import PlayerProfile


class TrainerDashboard(Trainer):
    class Meta:
        proxy = True

    def get_trainee_list(self):
        return self.trainees.all()
    
    def get_trainee_profile_info(self, trainee):
        profile = getattr(trainee, 'profile', None)
        info = {
            'name': trainee.user.get_full_name(),
            'phone_number': trainee.phone_number,
        }

        if profile:
            info.update({
                'current_xp': profile.current_xp,
                'level': profile.level.name if profile.level else None,
                'badges_count': profile.achievements.count(),
            })
        else:
            info.update({
                'current_xp': 0,
                'level': None,
                'badges_count': 0,
            })
        
        task_counts = (
            TaskAssignment.objects
            .filter(trainee=trainee, completed=True, due_date__lte=date.today())
            .values('task__type')
            .annotate(count=Count('id'))
        )
        info['task_counts'] = list(task_counts)

        fixed_sessions = trainee.fixed_sessions.values('day_of_week', 'location', 'start_time', 'end_time')
        info['fixed_sessions'] = list(fixed_sessions)

        appointments = AppointmentRequest.objects.filter(trainee=trainee, status='PENDING')
        info['appointment_requests'] = list(appointments.values())

        return info

    def add_extra_xp(self, trainee, xp):
        profile = getattr(trainee, 'profile', None)
        if profile:
            profile.current_xp += xp
            profile.save()
            return True
        return 'Profile not found'
    
    def _weekday_code(self, weekday_int):
        mapping = {
            0: 'MO',
            1: 'TU',
            2: 'WE',
            3: 'TH',
            4: 'FR',
            5: 'SA',
            6: 'SU',
        }
        return mapping.get(weekday_int, '')

    def todays_plan(self):
        today_code = self._weekday_code(date.today().weekday())
        sessions = FixedSession.objects.filter(trainee__trainer=self, day_of_week=today_code)
        return sessions.values('trainee__user__username', 'location', 'start_time', 'end_time')

    def tomorrows_plan(self):
        tomorrow_code = self._weekday_code((date.today() + timedelta(days=1)).weekday())
        sessions = FixedSession.objects.filter(trainee__trainer=self, day_of_week=tomorrow_code)
        return sessions.values('trainee__user__username', 'location', 'start_time', 'end_time')