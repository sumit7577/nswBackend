import random
import string
from django.contrib.auth.base_user import BaseUserManager
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from app.utils import *
from django.utils.translation import gettext_lazy as _

class CustomManager(BaseUserManager):
    use_in_migrations = True

    def generate_random_username(self):
        """
        Generate a unique random username.
        """
        while True:
            username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            if not self.model.objects.filter(username=username).exists():
                return username
            

    def _create_user(self, email=None, password=None, username=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            username = email.split("@")[0]+"_"+self.generate_random_username()
        
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, username, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        extra_fields.setdefault("phone",9117517982)
        return self._create_user(email,password,username, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()