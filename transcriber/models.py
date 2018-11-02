from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from google.cloud import storage
import random
import string


class ClientManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        def randword(length):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))

        def create_bucket(bucket_name):
            """Creates a new bucket."""
            storage_client = storage.Client()
            bucket = storage_client.create_bucket(bucket_name)
            print('Bucket {} created'.format(bucket.name))

        """Create and save a User with a given email and password."""
        user = self.model(email=email, bucket=create_bucket(randword(10)), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given emailnumber and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given emailnumber and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Client(AbstractUser):
    username = models.CharField(max_length=5, default="", unique=False)
    email = models.EmailField(unique=True)
    bucket_name = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.email)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ClientManager()


class Transcript(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    destination_blob_name = models.CharField(max_length=50, blank=True)
    source_file_name = models.CharField(max_length=50, blank=True)
    file = models.FileField(max_length=None)
    transcript = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.source_file_name, self.client)
