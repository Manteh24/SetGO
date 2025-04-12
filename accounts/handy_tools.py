def get_full_name_plus_username(user):
    return f"{user.first_name or ''} {user.last_name or ''} ({user.username})".strip()