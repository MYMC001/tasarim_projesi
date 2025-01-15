from django.db import models
from django.contrib.auth.models import User ,AbstractUser 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUser(AbstractUser):
     is_delivier=models.BooleanField(default=False )
     is_active_f_order=models.BooleanField(default=False)
     is_ban=models.BooleanField(default=False)
     deliver_num=models.IntegerField(default=0)

   

class Restaurant(models.Model):
     name=models.CharField(max_length=100  ,blank=False )
     user=models.OneToOneField('Jib.CustomUser',related_name='restaurant' ,on_delete=models.CASCADE)
     discription=models.CharField(max_length=100 , default='Burugur')
     adress=models.CharField(max_length=100)
     image=models.ImageField(upload_to='res_images/')
     type=models.CharField(max_length=10 ,default="Burgur")
     minimum=models.IntegerField(default=90)
     new_orders=models.IntegerField(default=0)
     date=models.DateTimeField(auto_now=True)
     likes=models.IntegerField(default=0)
     is_like=models.BooleanField(default=False)
     is_free=models.BooleanField(default=True)
     teslimat_ucreti=models.IntegerField(default=10)
     res_hizmet=models.IntegerField(default=11)
     orders_quantity=models.IntegerField(default=0)
     def __str__(self):
          return  self.name


class Address(models.Model):
     user=models.OneToOneField('Jib.CustomUser' ,related_name='addresses' ,on_delete=models.CASCADE)
     city=models.CharField(max_length=30)
     street=models.CharField(max_length=30)
     neighborhood =models.CharField(max_length=100)
     building_name=models.CharField(default='A' ,max_length=30)
     apartment_n=models.CharField(default=' d'  ,max_length=20)
     floor_num=models.IntegerField(default=0)
     phone=models.CharField(max_length=10 ,default= '')
     full_adress=models.TextField(default=' ' ,max_length=200)

     def __str__(self):
          return self.user.username

class Product(models.Model):
     name=models.CharField(max_length=100 ,blank=False)
     price=models.DecimalField(decimal_places=2 ,max_digits=10)
     discription=models.CharField(max_length=100)
     restaurant=models.ForeignKey(Restaurant ,related_name='product' ,on_delete=models.CASCADE )
     image=models.ImageField(upload_to='images/' )
     type=models.CharField(max_length=50 ,default='Drink')
     p_counter=models.IntegerField(default=0)
     def __str__(self):
          return self.name

class Order(models.Model):
    user = models.ForeignKey('Jib.CustomUser', related_name="orders", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name="orders", on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    is_on_way=models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_accepted=models.BooleanField(default=False)
    is_canceled=models.BooleanField(default=False)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    created_at = models.DateTimeField(auto_now=True)   
    is_tip=models.BooleanField(default=False)
    tip_value=models.IntegerField(default=0) 
    order_image=models.CharField(max_length=100 ,default= 'nothing')
    order_stepDes=models.CharField(max_length=100 ,default="none")
    Toplam=models.IntegerField(default=0)
    is_accepted_fd=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now=True)
    delivred_date=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class Payment(models.Model):
     order=models.OneToOneField(Order, related_name='payment' ,on_delete=models.CASCADE)
     is_payed=models.BooleanField(default=False)  
     payment_type=models.CharField(default='cash' ,max_length=40)  
     def __str__(self):
          return str(self.order.id)
     
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price=models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"    



class Favorite(models.Model):

     user=models.ForeignKey('Jib.CustomUser' ,related_name='favorite' ,on_delete=models.CASCADE)
     restaurant=models.ForeignKey(Restaurant ,related_name='favorite' ,on_delete=models.CASCADE)
     is_favorite=models.BooleanField(default=False)

     def __str__(self):
          return  str(self.id)
     


class User_Message(models.Model):
     sender=models.ForeignKey('Jib.CustomUser' ,related_name='messages' ,on_delete=models.CASCADE)
     receiver=models.ForeignKey('Jib.CustomUser' ,related_name='messagess'  ,on_delete=models.CASCADE)
     restaurant=models.ForeignKey(Restaurant ,related_name='r_messages' ,on_delete=models.CASCADE )
     value=models.CharField(max_length=100 ,default='None')
     date=models.TimeField(auto_now=True)

     def __str__(self):
          return self.user.username
     


class Order_Deliver(models.Model):

     user=models.ForeignKey('Jib.CustomUser' ,related_name='delivers' ,on_delete=models.CASCADE)
     order=models.ForeignKey(Order, related_name='deliver' ,on_delete=models.CASCADE)
     is_delivered=models.BooleanField(default=False )
     is_accept=models.BooleanField(default=False)
     image=models.ImageField(upload_to='orders_images/')
     
     def __str__(self):
          return self.user.username

     


class Wallet(models.Model):

     user=models.OneToOneField('Jib.CustomUser' ,related_name='wallet' ,on_delete=models.CASCADE)
     value=models.IntegerField(default=0)
     def __str__(self):
          return str(self.user.name)
