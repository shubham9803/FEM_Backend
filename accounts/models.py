from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid

class UserManager(BaseUserManager):
    def create_user(self, mobile, email, fname, lname, password=None):
        if not mobile:
            raise ValueError("Mobile number is required")

        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            mobile=mobile,
            email=email,
            fname=fname,
            lname=lname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, email, fname, lname, password):
        user = self.create_user(mobile, email, fname, lname, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Family(models.Model):
    name = models.CharField(max_length=255)

    code = models.CharField(
        max_length=10,
        unique=True,
        editable=False
    )

    created_by = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='families_created'
    )

    def generate_family_code(self):
        return f"FAM{uuid.uuid4().hex[:6].upper()}"

    def save(self, *args, **kwargs):
        if not self.code:
            while True:
                code = self.generate_family_code()
                if not Family.objects.filter(code=code).exists():
                    self.code = code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"


class User(AbstractBaseUser, PermissionsMixin):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

    family = models.ForeignKey(Family, null=True, blank=True, on_delete=models.SET_NULL,related_name='members')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['email', 'fname', 'lname']

    def __str__(self):
        return self.mobile


        