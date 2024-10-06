from django.db import models
import uuid
from django.contrib.auth.models import \
(
    AbstractBaseUser, 
    BaseUserManager,
    PermissionsMixin,
)
from core.abstract.models import AbstractManager, AbstractModel
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class UserManager(BaseUserManager, AbstractManager):
    
    def get_object_by_public_id(self, public_id):
        try:
            return  self.get(public_id=public_id)
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404
        
    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a User with an email, phone number, username and password
        """
        if username is None:
            raise TypeError("Users must have a username")
        if email is None:
            raise TypeError("Users must have an email")
        if password is None:
            raise TypeError("User must have an email")
        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user     
    
    def create_super_user(self, username, email, password=None, **kwargs):
        """Create and return a User with superUser (admin) permissions
        """
        if email is None:
            raise TypeError("Superusers  must have an email")
        if password is None:
            raise TypeError("Superuser must have an email")
        if username is None:
            raise TypeError("Superusers  must have a username")
        
        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staf = True
        user.save(using=self._db)
        return user    
        

class User(AbstractBaseUser, AbstractModel, PermissionsMixin):
    avatar = models.ImageField(null=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    bio = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS  = ['username']
    
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.email}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    


        
        
        