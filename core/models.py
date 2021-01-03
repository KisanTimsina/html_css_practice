from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True )
    mobile_number = models.IntegerField(null=True, blank=True)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.name:
            name = self.name
        elif self.device:
            name = self.device
        else: 
            name = self.user.username
        return name

CATEGORY_CHOICES = (
    ('F', 'Food'),
    ('SW', 'Sport Wear'),
    ('C', 'Clothes' ),
    ('BC', 'Boy Clothes'),
    ('GC', 'Girls Clothes')
)

LABEL_CHOICES = (

    ('B', 'primary'),
    ('P', 'secondary'),
    ('R', 'danger' )
    
)

class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True )
    before_price = models.IntegerField()
    now_price = models.IntegerField()
    image = models.ImageField(blank=False)
    catogory = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(default="product-1")
    description = models.TextField(default='write down your product infromation here!')

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

       
    def get_total_of_order_items(self):
        if self.item.now_price:
            return self.quantity * self.item.now_price
        else:
            return self.quantity * self.item.before_price

            
    def get_amount_saved(self):
        return (self.quantity * self.item.before_price) - (self.quantity * self.item.now_price)

    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True )
    name = models.CharField(max_length=50, null=True, blank=True )
    mobile_number = models.IntegerField(null=True, blank=True)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField( blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    
   
    def __str__(self):
        return f"{self.name} [{self.mobile_number}] with Total = {self.total_price()} Ks"

    def total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_of_order_items()
        return total 

    def total_saved(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_amount_saved()
        return total

    def get_items_total(self):
        total= 0
        for item in self.items.all():
            total += 1
        return total

    

 