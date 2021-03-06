from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
# Create your models here.

CATEGORY_CHOICES = (
    ('L','LG'),
    ('H','Huawei'),
    ('A','Apple'),
)


LABEL_CHOICES = (
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
)
class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    # category = models.CharField(choices=CATEGORY_CHOICES,max_length=2,default='SW')
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES,max_length=1,default='P')
    slug = models.SlugField(default='test-product')
    description = models.TextField(default='')
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to='products/',default=None,blank=True,null=True)
    def __str__(self):
        return self.title


    def get_category(self):
        CATEGORYS = []
        for c in CATEGORY_CHOICES:
            CATEGORYS.append(c[1])
        return CATEGORYS

    def get_absolute_url(self):
        return reverse('product',kwargs={
            'slug':self.slug
        })

    def get_add_to_card_url(self):
        return reverse('add-to-card',kwargs={
            'slug':self.slug
        })

    def delete_from_cart_url(self):
        return reverse('delete-from-card', kwargs={
            'slug': self.slug
        })




import  datetime
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} Of {self.item.title}"

    def get_total_item_price(self):

        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_discount_item_price() - self.get_total_item_price()

    # def get_final_price(self):
    #     if self.item.discount_price:
    #         return self.get_total_item_price()
    #     return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress',on_delete=models.SET_NULL,blank=True,null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    copon = models.ForeignKey('Copun',models.SET_NULL,blank=True,null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_request = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


    def get_total_item_all_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        if self.copon:
            total -= self.copon.amount
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)
    street_address =  models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    Stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Copun(models.Model):
    code = models.CharField(max_length=50)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f'{self.pk}'