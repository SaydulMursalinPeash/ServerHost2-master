from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser 

from django.contrib.contenttypes.models import ContentType

ContentType._meta.app_label = 'contenttypes'


    

class UserManager(BaseUserManager):
    def create_user(self, email, name,tc, password=None,password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,name,tc, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            tc=tc
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    #date_of_birth = models.DateField()
    name=models.CharField(max_length=200,unique=True)
    image=models.ImageField(upload_to='user/image/',null=True,blank=True)
    tc=models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_valid= models.BooleanField(default=False)
    is_officer=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()
    #stuff_users = StuffUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    def is_valid_user(self):
        return self.is_valid
    


class AccessToken(models.Model):
    token=models.TextField(max_length=1000,null=False,blank=False)
    type=models.CharField(max_length=50,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='token_user')
    time=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.name + self.type