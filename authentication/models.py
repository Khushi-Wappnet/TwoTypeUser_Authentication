from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

class Buyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_profiles')
    default_shipping_address = models.TextField(blank=True, null=True)
    wishlist_items = models.JSONField(default=list, blank=True)
    preferred_categories = models.JSONField(default=list, blank=True)
    loyalty_points = models.IntegerField(default=0)
    is_verified_buyer = models.BooleanField(default=False)

    def __str__(self):
        return f"Buyer Profile: {self.user.email}"

class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_profiles')
    store_name = models.CharField(max_length=100)
    business_registration_number = models.CharField(max_length=50)
    store_address = models.TextField()
    product_categories = models.JSONField(default=list, blank=True)
    is_verified_seller = models.BooleanField(default=False)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Seller Profile: {self.user.email}"