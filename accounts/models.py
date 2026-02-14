# accounts/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# Custom manager required for AbstractBaseUser — handles user creation logic
class UserManager(BaseUserManager):
    """Manager for the custom User model with email-based authentication."""

    def create_user(self, email, full_name, password=None, **extra_fields):
        """Create and return a regular user with hashed password."""
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)  # Lowercases the domain part
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)  # Hashes the password using Django's built-in hasher
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        """Create and return a superuser (admin) with elevated privileges."""
        extra_fields.setdefault('user_type', 'Admin')
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, full_name, password, **extra_fields)


class User(AbstractBaseUser):
    """
    Custom user model using email for authentication instead of username.
    Inherits 'password' and 'last_login' from AbstractBaseUser — no need for a separate password field.
    """

    # Choices for user_type — must match DB CHECK constraint exactly
    USER_TYPE_CHOICES = [
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
        ('Staff', 'Staff'),       # Present in DB script CHECK constraint
        ('Admin', 'Admin'),
    ]

    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)  # Matches DB column — used for security/hashing
    # NOTE: AbstractBaseUser also provides a 'password' field used by Django auth internally
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='Student')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Matches DB DEFAULT CURRENT_TIMESTAMP

    USERNAME_FIELD = 'email'  # Log in with email since there's no username column
    REQUIRED_FIELDS = ['full_name']  # Fields prompted during createsuperuser (besides email & password)

    objects = UserManager()  # Attach the custom manager

    class Meta:
        db_table = 'Users'  # Matches the exact database table name

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Role(models.Model):
    """Represents a role that can be assigned to users (e.g., President, Coordinator)."""
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'Roles'

    def __str__(self):
        return self.role_name


class UserRole(models.Model):
    """Junction table linking users to their roles (many-to-many through table)."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        db_column='user_id',
        related_name='user_roles'  # Access via user.user_roles.all()
    )
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE,
        db_column='role_id',
        related_name='role_users'  # Access via role.role_users.all()
    )

    class Meta:
        db_table = 'User_Roles'
        unique_together = (('user', 'role'),)  # Prevents duplicate role assignments

    def __str__(self):
        return f"{self.user.full_name} — {self.role.role_name}"