from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator

class CustomUser(AbstractUser):
    is_owner = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(10, message="Phone number must be exactly 10 digits."),
            RegexValidator(r'^\d{10}$', message="Phone number must contain only digits.")
        ],null=True
    )

    def __str__(self):
        return self.name

class Jewelry(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='jewelry_images/')
    CATEGORY_CHOICES = [
        ('Necklace', 'Necklace'),
        ('Earrings', 'Earrings'),
        ('Bracelet', 'Bracelet'),
        ('Ring', 'Ring'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="Uncategorized")

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    jewelry = models.ForeignKey(Jewelry, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], 
        default='Pending'
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
