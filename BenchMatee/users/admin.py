from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,GamificationProfile,Badge,Friendship

# Register your models here.
# admin for Gamification
class GamificationProfileInline(admin.StackedInline):
    model = GamificationProfile
    can_delete = False
    verbose_name = 'Gamification Profile'
    fields = ('xp','level','badges','current_streaks','last_login_data')

# custom admin for User
class UserAdmin(BaseUserAdmin):
    # adding the gamification profile to User change page

    # showing the custom fields
    fieldsets = BaseUserAdmin.fieldsets +(
        (None,{'fields': ('name','school',)}),
    )

admin.site.register(User,UserAdmin)
admin.site.register(Badge)
admin.site.register(Friendship)