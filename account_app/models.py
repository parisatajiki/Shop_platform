from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None, full_name="کاربر بدون نام"):
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            username=username,
            email=email,
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="آدرس ایمیل",
        max_length=255,
        unique=True,
        null=True,
        blank=True,

    )
    full_name = models.CharField(verbose_name="نام کامل", max_length=50, default="کاربر بدون نام")
    username = models.CharField(verbose_name="نام کابری", max_length=50,unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name=" ادمین ")

    objects = UserManager()

    USERNAME_FIELD = "username"  # اون فیلدی که میخواهیم بر اساس ان احراز هویت و لاگین و... انجام شود و البته ان فیلد حتما باید یونیک ترو باشد
    REQUIRED_FIELDS = []  # فیلدی که اجباری اشت و حتما باید پر شود

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = " کاربر "
        verbose_name_plural = " کاربرها "

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


from django.utils import timezone
from datetime import timedelta


class PendingUser(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

