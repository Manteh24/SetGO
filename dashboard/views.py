from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import TrainerDashboard

@login_required
def trainer_dashboard(request):
    try:
        # Use the proxy model so that our custom methods are available.
        trainer = TrainerDashboard.objects.get(user=request.user)
    except TrainerDashboard.DoesNotExist:
        # In case the logged-in user is not set up as a Trainer.
        return render(request, 'dashboard/error.html', {
            'message': 'Trainer profile not found.'
        })

    # Get trainees and build a list of profile info dictionaries
    trainees = trainer.get_trainee_list()
    trainee_profiles = []
    for trainee in trainees:
        trainee_profiles.append(trainer.get_trainee_profile_info(trainee))

    context = {
        'trainer': trainer,  # You can use this in the template if needed.
        'trainee_profiles': trainee_profiles,
        'today_sessions': trainer.todays_plan(),
        'tomorrow_sessions': trainer.tomorrows_plan(),
    }
    return render(request, 'dashboard/trainer_dashboard.html', context)