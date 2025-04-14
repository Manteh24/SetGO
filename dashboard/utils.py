from venv import logger
from django.db.models import Count
from datetime import date
from appointments.models import AppointmentRequest
from tasks.models import TaskAssignment


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
