from datetime import date, timedelta
from venv import logger
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
            'name': f"{trainee.user.first_name} {trainee.user.last_name}",
            'phone_number': trainee.phone_number,
            'current_xp': 0,
            'level': None,
            'level_number': None,
            'badges_count': 0,
        }

        if profile:
            level = profile.level
            info.update({
                'current_xp': profile.current_xp,
                'level': level.name if level else None,
                'level_number': level.number if level else None,
                'badges_count': profile.achievements.count(),
            })
        else:
            # Log a warning if the profile is missing
            logger.warning(f"Trainee {trainee} has no profile associated.")

        # The rest of your information:
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
    

class TraineeDashboard(Trainee):
    class Meta:
        proxy = True

    def get_profile_info(self):

        profile = getattr(self, 'profile', None)
        info = {
            'name': f"{self.user.first_name} {self.user.last_name}",
            'trainer': str(self.trainer) if self.trainer else None,
            'level': None,
            'level_name': None,
            'xp': 0,
            'badges': [],
        }

        if profile:
            level = profile.level
            info['xp'] = profile.current_xp
            if level:
                info['level'] = level.number
                info['level_name'] = level.name
            # Using the many-to-many relationship via PlayerProfile.achievements.
            info['badges'] = list(profile.achievements.values_list('name', flat=True))
        return info

    def get_assigned_tasks(self):

        return TaskAssignment.objects.filter(trainee=self)

    def mark_task_done(self, task_assignment_id):
        try:
            assignment = TaskAssignment.objects.get(id=task_assignment_id, trainee=self)
            assignment.completed = True
            assignment.save()
            return True
        except TaskAssignment.DoesNotExist:
            return False

    def send_appointment_request(self, req_date, start_time, end_time, message=None):
        if not self.trainer:
            raise ValueError("No trainer associated with this trainee.")
        appointment = AppointmentRequest.objects.create(
            trainee=self,
            trainer=self.trainer,
            date=req_date,
            start_time=start_time,
            end_time=end_time,
            status='PENDING',
            message=message,
        )
        return appointment
