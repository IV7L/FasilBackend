import hashlib
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
import math
import random
from django.core.validators import MinValueValidator, MaxValueValidator


TEAM_STATUS = (
    ('1','Active'),
    ('2','Not Active'),
    ('3','Finsihed'),
)

TEAM_TYPE = (
    ('1','Support'),
    ('2','Opposing'),
    ('3','Not Defined')
)

def random_nonce_for_account():
    return math.floor(random.random() * 1000000)

def random_nonce_for_member():
    return math.floor(random.random() * 1000000)

def random_nonce_for_invitation():
    return math.floor(random.random() * 1000000)
    
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, password=None, ethereum_address=None):
        if not username and not ethereum_address:
            raise ValueError('At least one of username, or ethereum address must be provided')

        user = self.model(
            username=username,
            ethereum_address=ethereum_address,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, ethereum_address=None):
        user = self.create_user(
            password=password,
            ethereum_address=ethereum_address,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=255) # add on utilites section in frontend
    ethereum_address = models.CharField(max_length=255, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True) # add on utilites section in frontend
    phone_number = models.IntegerField(null=True) # add on utilites section in frontend
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='default_profile_pic.png')
    
    USERNAME_FIELD = 'ethereum_address'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return self.full_name if self.full_name else self.ethereum_address if self.ethereum_address else ''

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

class DebateMember(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    debate = models.ForeignKey(to='debate_app.debate', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    enrolled = models.BooleanField(default=False)
    invitation_code = models.IntegerField(default=random_nonce_for_invitation, null=True)
    member_order = models.IntegerField(null=True,validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self) -> str:
        return self.account.ethereum_address

class DebateViewers(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    debate = models.ForeignKey(to='debate_app.debate', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    has_vote = models.BooleanField(default=False)
    vote_code = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'This account {self.account.ethereum_address} as a viewer'
    
class Team(models.Model):
    status = models.CharField(choices=TEAM_STATUS, max_length=255, default='2')
    type = models.CharField(choices=TEAM_TYPE, max_length=255, default='3')
    member = models.ManyToManyField(to=DebateMember, blank=True)
    recess_room1 = models.ForeignKey(to='quote.RecessRoom', on_delete=models.SET_NULL, null=True, default=None, blank=True, related_name='RecessRoomType1')
    recess_room2 = models.ForeignKey(to='quote.RecessRoom', on_delete=models.SET_NULL, null=True, default=None, blank=True, related_name='RecessRoomType2')

    def __str__(self) -> str:
        return self.get_status_display() + ' ' + self.get_type_display()

# @receiver(post_save, sender=DebateMember)
def save_profile(sender, instance, **kwargs):
    if instance.enrolled == True and not Account.objects.filter(ethereum_address = instance.ethereum_address):
        Account.objects.create(
            username=instance.full_name,
            public_address=instance.public_address,
            nonce=instance.nonce,
        )
    try:
        get_team_if_enrolled = instance.team
        get_all_team_members = DebateMember.objects.filter(team=get_team_if_enrolled)
        overall_status = True

        for mem in get_all_team_members:
            if mem.enrolled == False:
                overall_status = False
            else:
                pass

        if overall_status == True:
            instance.team.status = '1'
            instance.team.save()
    except:
        return 'wtf'