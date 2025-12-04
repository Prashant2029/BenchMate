from .models import UserProfile

RANK_THRESHOLDS = {
    'Novice': 0,
    'Apprentice': 100,
    'Scholar': 500,
    'Master': 1000,
    'Grandmaster': 5000,
}

def calculate_rank(xp):
    current_rank = 'Novice'
    for rank, threshold in RANK_THRESHOLDS.items():
        if xp >= threshold:
            current_rank = rank
    return current_rank

def award_xp(user, amount):
    profile = user.profile
    profile.xp += amount
    profile.weekly_xp += amount
    
    # Simple level calculation: 1 level per 100 XP
    profile.level = (profile.xp // 100) + 1
    
    profile.rank = calculate_rank(profile.xp)
    profile.save()
