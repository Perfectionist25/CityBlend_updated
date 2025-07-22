from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'kafe_categories'

class Food(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    price = models.IntegerField()
    is_new = models.BooleanField(default=False)
    is_discounted = models.BooleanField(default=False)
    category = models.ForeignKey('kafe.Category', on_delete=models.CASCADE)
    thumb = models.ImageField(default='default.png', null=True)

    def __str__(self):
        return self.title
    
    def comment_count(self):
        return Review.objects.filter(food=self).count()

    class Meta:
        db_table = 'kafe_foods'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Food)

class Slide(models.Model):
    image = models.ImageField(default='slide.jpg')


class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        
        return self.food.title

    def total_price(self):
        return self.food.price * self.quantity
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    phone = models.CharField(max_length=13)
    total_price = models.IntegerField()

    def str(self):
        return f"Order #{self.pk}"
    
class OrderFood(models.Model):
    order = models.ForeignKey('kafe.Order', on_delete=models.CASCADE, related_name='order_food')
    food = models.ForeignKey('kafe.Food', on_delete=models.CASCADE)
    amount = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return f"{self.food} x{self.amount} - {self.order.customer.username}"

RATE_CHOICES = [
    (5, '⭐️⭐️⭐️⭐️⭐️'),
    (4, '⭐️⭐️⭐️⭐️'),
    (3, '⭐️⭐️⭐️'),
    (2, '⭐️⭐️'),
    (1, '⭐️'),
]

class Review(models.Model):
    # profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    text = models.TextField(blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return self.user.username
