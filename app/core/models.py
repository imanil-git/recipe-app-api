"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    """Manage for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User (AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipe."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Specialization(models.Model):
    """Medical Specialization created by a user."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='specializations'
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    specialty = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  #Auto-generate slug from name
        super().save(*args, **kwargs)   #Call the real save method

    def __str__(self):
        return self.name


# class Country(models.Model):
#     name = models.CharField(max_length=100)
#     abbr = models.CharField(max_length=10)
#     slug = models.SlugField()

#     def __str__(self):
#         return self.name


# class State(models.Model):
#     name = models.CharField(max_length=100)
#     abbr = models.CharField(max_length=10)
#     slug = models.SlugField()
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


# class City(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField()
#     lat = models.FloatField()
#     lng = models.FloatField()
#     state = models.ForeignKey(State, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


# class Doctor(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField()
#     description = models.TextField(blank=True)
#     address = models.CharField(max_length=255)
#     postal_code = models.CharField(max_length=20)
#     website = models.URLField(blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True)
#     lat = models.FloatField()
#     lng = models.FloatField()
#     timezone = models.CharField(max_length=50)
#     city = models.ForeignKey(City, on_delete=models.CASCADE)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     state = models.ForeignKey(State, on_delete=models.CASCADE)
#     is_premium = models.BooleanField(default=False)
#     appointment_cost = models.FloatField(blank=True, null=True)
#     source = models.CharField(max_length=50, blank=True)

#     def __str__(self):
#         return self.name
