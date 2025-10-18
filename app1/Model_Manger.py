from django.contrib.auth.models import BaseUserManager

class CostemUserManger(BaseUserManager):
    def CreatOfficerUser(self,email,password,**extra):
        if not email:
            raise ValueError('The Email field must be set')
        email=self.normalize_email(email)
        officer=self.model(email=email,**extra)
        officer.set_password(password)
        officer.save(using=self._db)
        return officer
    def create_superuser(self,email,password,**extra):
        extra.setdefault('is_staff',True)
        extra.setdefault('is_superuser',True)
        extra.setdefault('is_active',True)
        return self.CreatOfficerUser(email,password,extra)
