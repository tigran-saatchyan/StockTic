from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for the custom user model.

    This manager provides methods for creating both regular users and
    superusers.

    Methods:
        create_user(email, password=None, **extra_fields):
            Create and save a regular user.

        create_superuser(email, password=None, **extra_fields):
            Create and save a superuser.

    Usage:
        - Use this custom user manager for the custom user
        model to handle user creation.

    Example:
        ```python
        from django.contrib.auth.models import BaseUserManager

        class CustomUserManager(BaseUserManager):
            ...
        ```
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user.

        Args:
            email (str): The user's email address.
            password (str): The user's password.
            **extra_fields: Additional user fields.

        Returns:
            User: The created regular user.

        Raises:
            ValueError: If the email is not provided.

        Usage:
            Create a regular user using this method.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser.

        Args:
            email (str): The superusers email address.
            password (str): The superusers password.
            **extra_fields: Additional superuser fields.

        Returns:
            User: The created superuser.

        Raises:
            ValueError: If is_staff or is_superuser is not set to True.

        Usage:
            Create a superuser using this method.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
