from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
#  bang phan loai hang hao
class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name="sub_categories", null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100,unique=True)
    def __str__(self):
        return self.name
class Changeform(UserCreationForm):
    class Meta:
        model= User 
        fields = ['username', 'email','first_name', 'last_name','password1','password2']
# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
#     name = models.CharField(max_length=100, null=True, blank=True)
#     email = models.EmailField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return self.name
class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='product')
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(null=True, blank=False, help_text="Đơn vị: VND")
    image = models.ImageField(null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    detail = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name
    # điều chỉnh thuộc tính 
    @property 
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = 'app/images/placeholder.png'
        return url


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    day = models.DateTimeField(auto_now_add=True) 
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id)
    #  đếm số lượng sản phẩm 
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    # tính tổng tiền
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=False)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    day_added = models.DateTimeField(auto_now_add=True)
# tính tổng tiền của từng sản phẩm
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    additional_address = models.CharField(max_length=200, null=True, blank=False)
    country = models.CharField(max_length=200, null=True, blank=True)
    day_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


