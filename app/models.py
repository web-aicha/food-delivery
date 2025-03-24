from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category_images/',null=True, blank=True)
    
    def __str__(self) :
        return self.name
    
class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField()
    rating = models.IntegerField()
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True) 
    
    def __str__(self):
        return self.name
    
    
class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="cart",default=1
    )  # Each user has only one cart
    subtotal = models.FloatField(default=0.0)
    delivery_fee = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def update_totals(self):
      self.subtotal = sum(item.menu_item.price * item.quantity for item in self.cart_items.all())
      self.delivery_fee = 2.00  # Example, you can customize
      self.total = self.subtotal + self.delivery_fee
      self.save()


    @staticmethod
    def get_or_create_cart(user):
        """Returns the existing cart for a user or creates a new one."""
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    
    def get_total_price(self):
        return self.menu_item.price * self.quantity
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_totals()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.cart.update_totals()
        
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in Cart {self.cart.id}"
    

class Delivery(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name="delivery")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    is_delivered = models.BooleanField(default=False)  # Track delivery status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery for Cart #{self.cart.id}"