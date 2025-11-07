from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, GamificationProfile, Badge

@receiver(post_save,sender=User)
def user_and_badge(sender, instance, created, **kwargs):
    # check if user created
    if created:
        profile = GamificationProfile.objects.create(user=instance)

        # assigning the rookie badge
        try:
            rookie_badge = Badge.objects.get(slug="rookie-starter")
            profile.badges.add(rookie_badge)
                
        except Badge.DoesNotExist:
            print("Rookie Badge not found!")