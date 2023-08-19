from django.db import models
import uuid
import base64
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import time
import random
from django.utils import timezone
from datetime import timedelta
import phonenumbers


def get_code(num):
    print('▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣','','','','','','Код:',num,'','','','','','','▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣',sep='\n')


class UserManager(BaseUserManager):


    def create_user(self, phone_number,password=None, referred_by=None):

        if not phone_number:
            raise ValueError('Users must have an phone')

        user = self.model(
            phone_number=phone_number,
            referred_by=referred_by
        )
        user.save(using=self._db)

        return user

    def create_staffuser(self, phone_number,password=None, referred_by=None):

        if not phone_number:
            raise ValueError('Users must have an phone')

        user = self.model(
            phone_number=phone_number,
            referred_by=referred_by,
        )
        user.staff=True
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number,password=None, referred_by=None):

        if not phone_number:
            raise ValueError('Users must have an phone')

        user = self.model(
            phone_number=phone_number,
            # invite_code=base64.urlsafe_b64encode(uuid.uuid1().bytes).decode("utf-8")[:6],
            referred_by=referred_by,
        )
        user.set_password(password)
        user.staff=True
        user.admin=True
        user.save(using=self._db)

        return user
    
class User(AbstractBaseUser):




    phone_number = models.CharField(max_length=15, unique=True)

    invite_code = models.CharField(blank=True,max_length=6, null=True,unique=True,)
    referred_by = models.ForeignKey('self',blank=True, on_delete=models.SET_NULL, null=True, related_name='referrals')
    is_active = models.BooleanField(blank=True,default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False) 
    password=models.TextField(blank=True,default='nothing',null=True)
    auth_code_1 = models.CharField(max_length=4,null=False,blank=True,default='')
    auth_code_2 = models.CharField(max_length=4,null=False,blank=True,default='')
    auth_data = models.DateTimeField(null=False,auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [] 

    objects = UserManager()



    def get_phone_number(self):
        return self.phone_number

    def get_invite_code(self):
        return self.invite_code
    
    def get_referred_code(self):
        return self.referred_by

    def __str__(self):
        return str(self.pk)+' '+self.invite_code

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def has_usable_password(self):
        return False

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
    
    def save(self, *args, **kwargs):


        if not self.invite_code:
            self.invite_code = base64.urlsafe_b64encode(uuid.uuid1().bytes).decode("utf-8")[:6]
        
        current_datetime = timezone.now()

        if not self.admin and not self.auth_code_1:
            self.set_password("nothing")
            self.auth_code_1=''.join(str(random.randint(0, 9)) for _ in range(4))
            get_code(self.auth_code_1)
            self.auth_data=current_datetime + timedelta(minutes=1)

        
        super().save(*args, **kwargs)

    class Meta:

        managed = True
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователь'
        unique_together = (('invite_code', 'referred_by'),)
    
    