from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse

# Create your models here.

# These are basically instructions for django to create actual tables in the database
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=225,db_index=True)               #db_index-->??
    slug = models.SlugField(max_length=225, unique=True)                #SlugField,unique--->??
    category_image = models.ImageField(upload_to='uploads/ategory', default='uploads/products/default.jpg')

    class Meta:                                                         #Meta-->??
        verbose_name_plural='categories'
    
    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User , on_delete=models.CASCADE , related_name='product_creator')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    description = models.CharField(
        max_length=1000, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/',default='uploads/products/default.jpg')
    image2 = models.ImageField(upload_to='uploads/products/',default='uploads/products/default.jpg')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering=('created',)
    
    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])
    
    def __str__(self):
        return self.title
    
    @staticmethod                                                       #@staticmethod-->??
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)
  
    @staticmethod
    def get_all_products():
        return Product.objects.all()
  
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()



class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)
  
    # to save the data
    def register(self):
        self.save()
  
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
  
    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        
        return False
    
class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.today)
    status = models.BooleanField(default=False)
  
    def placeOrder(self):
        self.save()
  
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')