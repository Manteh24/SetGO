from . models import Level
from . models import PlayerProfile, Badge, PlayerBadge
from tasks.models import TaskAssignment


def show_level_progress(player_profile):

    level = player_profile.level
    if not level:
        return "No level assigned."
    
    current_xp = player_profile.current_xp
    xp_threshold_for_current_level = level.xp_threshold

    next_level = Level.objects.filter(number=level.number + 1).first()

    if next_level:
        xp_threshold_for_next_level = next_level.xp_threshold
        current_level_xp = current_xp - xp_threshold_for_current_level
        remaining_required_xp_for_current_level = xp_threshold_for_next_level - xp_threshold_for_current_level
        progress = f"{current_level_xp} / {remaining_required_xp_for_current_level}"
    else:
        progress = f"{current_xp} XP (Max level reached)"

    return progress



def evaluate_badges(player_profile):
    trainee = player_profile.trainee
    current_level = player_profile.level
    current_xp = player_profile.current_xp
    days_active = (date.today() - trainee.user.date_joined.date()).days

    newly_awarded = []

    for badge in Badge.objects.all():
        # Skip if already awarded
        if PlayerBadge.objects.filter(profile=player_profile, badge=badge).exists():
            continue

        # Check Level Requirement
        if badge.level_required and (not current_level or current_level.number < badge.level_required.number):
            continue

        # Check XP Requirement
        if badge.xp_required and current_xp < badge.xp_required:
            continue

        # Check Task Count (any completed task)
        if badge.specific_task_count:
            completed_task_count = TaskAssignment.objects.filter(
                trainee=trainee,
                completed=True
            ).count()

            if completed_task_count < badge.specific_task_count:
                continue

        # Check Days Active
        if badge.days_active_required and days_active < badge.days_active_required:
            continue

        # All requirements passed — award the badge
        PlayerBadge.objects.create(profile=player_profile, badge=badge)
        newly_awarded.append(badge)

    return newly_awarded
