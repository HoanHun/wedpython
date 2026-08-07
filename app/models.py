from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import os
from django.templatetags.static import static

# Create your models here.
#  bang phan loai hang hao
class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name="sub_categories", null=True, blank=True, verbose_name="Danh mục cha")
    is_sub = models.BooleanField(default=False, verbose_name="Là danh mục phụ")
    name = models.CharField(max_length=100, null=True, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug (Đường dẫn)")
    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục sản phẩm"
    def __str__(self):
        return self.name or ''
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
    category = models.ManyToManyField(Category,related_name='product', verbose_name="Danh mục", blank=True)
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tên sản phẩm')
    price = models.BigIntegerField(default=0, verbose_name="Giá", help_text="Đơn vị: VND")
    image = models.ImageField(null=True, blank=True,verbose_name="Hình ảnh")
    digital = models.BooleanField(default=False, null=True, blank=False,verbose_name='số sản phẩm')
    detail = models.TextField(null=True,blank=True,verbose_name="Mô tả chi tiết")
    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Danh sách sản phẩm"
    def __str__(self):
        return self.name or ''
    # điều chỉnh thuộc tính 
    @property 
    # def ImageURL(self):
    #     try:
    #         url = self.image.url
    #     except:
    #         url = ''
    #     return url            
    # 
    # # Kiểm tra an toàn xem trường image có dữ liệu và tên file không nếu có
    # Mặc định nếu lỗi/không có ảnh thì dùng ảnh placeholder ảnh mặt định này

    def static_image_path(self):
        try:
            if self.image and hasattr(self.image, 'name') and self.image.name:
                filename = os.path.basename(str(self.image.name)).lower()
                # Tự động xóa chuỗi mã hóa 7 ký tự ngẫu nhiên do Django Admin thêm vào (VD: _eouitfp)
                clean_name = re.sub(r'_[a-z0-9]{7}(?=\.)', '', filename)
                return f"app/images/{clean_name}"
        except Exception:
            pass
        return "app/images/placeholder.png"
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Khách hàng")
    day = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt") 
    complete = models.BooleanField(default=False, null=True, blank=False, verbose_name="Đã hoàn thành")
    transaction_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="Mã giao dịch")
    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Quản lý đơn hàng"
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
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Sản phẩm")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Đơn hàng")
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name="Số lượng")
    day_added = models.DateTimeField(auto_now_add=True, verbose_name="Ngày thêm")
    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"
# tính tổng tiền của từng sản phẩm
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Khách hàng")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Đơn hàng")
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name="Địa chỉ")
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name="Thành phố")
    state = models.CharField(max_length=200, null=True, blank=True, verbose_name="Tỉnh/Thành")
    mobile = models.CharField(max_length=10, null=True, blank=True, verbose_name="Số điện thoại")
    additional_address = models.CharField(max_length=200, null=True, blank=False, verbose_name="Địa chỉ bổ sung")
    country = models.CharField(max_length=200, null=True, blank=True, verbose_name="Quốc gia")
    day_added = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    class Meta:
        verbose_name = "Địa chỉ giao hàng"
        verbose_name_plural = "Địa chỉ giao hàng"
    def __str__(self):
        return self.address


