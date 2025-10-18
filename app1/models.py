from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class CostemUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active',False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class Socity(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    join_link = models.URLField()
    initials = models.CharField(max_length=10, default='ieee socity')
    img = models.ImageField(upload_to='posts/', null=True, blank=True, default='images/default.png')
    header=models.ImageField(upload_to='posts/', null=True, blank=True, default='images/default.png')

    def __str__(self):
        return self.name
    
    
    @property
    def officers(self):
        return self.socity_officer_set.all()

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    Academic_Year = [
        ('4', 'Fourth year'),
        ('3', 'Third year'),
        ('2', 'Second year'),
        ('1', 'First year'),
        ('Else', 'Else'),
    ]
    
    socity = models.ForeignKey(Socity, on_delete=models.CASCADE, null=True, blank=True)
    academic_year = models.CharField(max_length=10, choices=Academic_Year)
    major = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CostemUserManager()

    def __str__(self):
        return self.email

class Post(models.Model):
    socity = models.ForeignKey(Socity, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    img = models.ImageField(upload_to='posts/', null=True, blank=True)
    Posting_Date=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
class Socity_officer(models.Model):
    socity = models.ForeignKey(Socity, on_delete=models.CASCADE)
    officer_name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='officers/')
    position = models.CharField(max_length=100, blank=True) 
    
    def __str__(self):
        return f"{self.officer_name} - {self.socity.name}"
    
class branch_officer(models.Model):
    Name = models.CharField(max_length=100)
    Position = models.CharField(max_length=100)
    img = models.ImageField(upload_to='officers/')
    Linkedin=models.URLField(default='https://www.linkedin.com/feed/')
    
    def __str__(self):
        return self.Name