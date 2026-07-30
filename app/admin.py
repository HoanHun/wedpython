from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header = "Hệ Thống Quản Lý Bán Hàng"
admin.site.site_title = "Trang Quản Trị"
admin.site.index_title = "Quản lý sản phẩm và đơn hàng"
# admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
