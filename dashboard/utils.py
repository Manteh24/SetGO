from venv import logger
from django.db.models import Count
from datetime import date
from appointments.models import AppointmentRequest
from tasks.models import TaskAssignment


def get_trainee_profile_info(trainee):
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

def get_appointment_requests(self, user_type, status):
    today = date.today()
    filters = {'status': status, 'date__gte': today}

    if user_type == 'trainer':
        filters['trainer'] = self
        values = ['id', 'trainee__user__username', 'date', 'start_time', 'end_time', 'message']
    elif user_type == 'trainee':
        filters['trainee'] = self
        values = ['id', 'trainer__user__username', 'date', 'start_time', 'end_time', 'message']
    else:
        raise ValueError("Invalid user_type. Must be 'trainer' or 'trainee'.")

    requests = AppointmentRequest.objects.filter(**filters)
    return {status.lower(): requests.values(*values)}

def approve_appointment_request(self, appointment_id):
    try:
        appointment = AppointmentRequest.objects.get(id=appointment_id, trainer=self)
        appointment.status = 'APPROVED'
        appointment.save()
        return {'success': True, 'message': 'Appointment approved successfully.'}
    except AppointmentRequest.DoesNotExist:
        return {'success': False, 'message': 'Appointment not found.'}

def reject_appointment_request(self, appointment_id):
    try:
        appointment = AppointmentRequest.objects.get(id=appointment_id, trainer=self)
        appointment.status = 'REJECTED'
        appointment.save()
        return {'success': True, 'message': 'Appointment rejected successfully.'}
    except AppointmentRequest.DoesNotExist:
        return {'success': False, 'message': 'Appointment not found.'}

def reject_and_counteroffer_appointment_request(self, appointment_id, new_date, new_start_time, new_end_time):
    try:
        appointment = AppointmentRequest.objects.get(id=appointment_id, trainer=self)
        appointment.status = 'COUNTEROFFER'
        appointment.counteroffer_date = new_date
        appointment.counteroffer_start_time = new_start_time
        appointment.counteroffer_end_time = new_end_time
        appointment.save()
        return {'success': True, 'message': 'Counteroffer made successfully.'}
    except AppointmentRequest.DoesNotExist:
        return {'success': False, 'message': 'Appointment not found.'}

