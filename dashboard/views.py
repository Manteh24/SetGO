from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import TrainerDashboard

@login_required
def trainer_dashboard(request):
    try:
        # Use the proxy model to obtain our extended Trainer methods.
        trainer = TrainerDashboard.objects.get(user=request.user)
    except TrainerDashboard.DoesNotExist:
        return render(request, 'dashboard/error.html', {
            'message': 'Trainer profile not found.'
        })

    trainee_profiles = trainer.get_trainee_profile_info()

    context = {
        'trainer': trainer,
        'trainee_profiles': trainee_profiles,
        'today_sessions': trainer.todays_plan(),
        'tomorrow_sessions': trainer.tomorrows_plan(),
        'pending_appointments': trainer.get_pending_and_approved_appointments(),
        'approved_appointments': trainer.get_pending_and_approved_appointments(),
    }
    return render(request, 'dashboard/trainer_dashboard.html', context)
