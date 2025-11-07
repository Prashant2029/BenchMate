from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# User class
class User(AbstractUser):
    # student specific profile
    # inherits uername, first_name, last_name, email and password

    # custom fileds
    name = models.CharField(max_length=255, blank = False, null = False, help_text= "Full name of the User")
    school = models.CharField(max_length=255, blank= True, null = True, help_text="School of the user if associated")

    # print user
    def __str__(self):
        return self.username
    
# badges invloved
class Badge(models.Model):
    # badges earned by users
    name = models.CharField(max_length=255, blank=False, null= False, unique = True)
    description = models.TextField()
    icon_url = models.FileField(upload_to = 'badges/') # or file field
    slug = models.SlugField(unique=True, help_text="Unique Identifier")

    def __str__(self):
        return self.name

# Gamification class
class GamificationProfile(models.Model):
    # one - one relationship with user, holds thier gamified porfile for the platform

    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'gamification_profile')

    # gamification fields
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveSmallIntegerField(default = 1)

    # badges for users many - many 
    badges = models.ManyToManyField(Badge,blank=True)

    # streak fields
    current_streaks = models.PositiveIntegerField(default=0)
    last_login_data = models.DateField(blank=True,null=True )

    # print GamificationProfile
    def __str__(self):
        return f"{self.user.username}'s Profile {self.level}"
    

# friendship relation
class Friendship(models.Model):
    # friend relations between users

    # defining the status
    available_status = [
        ('PENDING','Pending'),
        ('ACCEPTED','Accepted'),
        ('BLOCKED','Blocked'),
    ]

    user1 = models.ForeignKey(User,on_delete=models.CASCADE, related_name='initiated_friendship')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accepted_friendship')

    status = models.CharField(max_length=20, choices=available_status, default = "PENDING")

    class Meta:
        unique_together = ('user1','user2') 
        # forces that a  friendship is unique avoiding situation like (A,B) and (B,A) as different

    # implementing class methods for avoiding duplicated requests
    @classmethod
    def get_existing_friendship(cls,usera,userb):
        # check for existing friend status
        friendship = cls.objects.filter(user1 = usera, user2 = userb).first()

        if not friendship:
            friendship = cls.objects.filter(user1= userb, user2= usera).first()
        
        return friendship
    
    @classmethod
    def creat_friend_request(cls,sender,reciever):
        # create a pending request

        existing_status = cls.get_existing_friendship(sender,reciever)

        if existing_status:
            return existing_status, False
        
        else:
            new_request = cls.objects.create(user1= sender, user2 = reciever)
            return existing_status,True

    def __str__(self):
        return f"{self.user1} and {self.user2} are in status {self.status}."
