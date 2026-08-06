from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm

# 
def detail(request):
    # Nếu model Order nối với Customer thì dùng request.user.customer
    if request.user.is_authenticated:
        customer = getattr(request.user, 'customer', request.user)  # Lấy đối tượng Customer từ User
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
        user_not_login = 'hidden'
        user_login = 'show'
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']
        user_not_login = 'show'
        user_login = 'hidden'
    id = request.GET.get('id','')
    product = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub = False)
    context = {'categories':categories,'product':product,'items': items, 'order': order, "cartitems": cartitems,'user_not_login': user_not_login, 'user_login': user_login}
    return render(request , 'app/xemct.html', context)
def category(request): #locj
    categories = Category.objects.filter(is_sub = False)
    active_cr = request.GET.get('category','')
    if active_cr:
        products = Product.objects.filter(category_slug = active_cr)
    context = {'categories':categories,'products': products,'active_cr': active_cr}
    return render(request, 'app/category.html', context)
def search(request):
    if request.method == 'POST':
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = getattr(request.user, 'customer', request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']
    products = Product.objects.all()
    return render(request,'app/timkiem.html',{"searched": searched, "keys": keys,'products': products, "cartitems": cartitems})
    
def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dangnhap")
    context = {'form':form}
    return render(request, 'app/dangky.html', context)
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password= password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'chua dung tai khoan hoac mat khau')
    context = {}
    return render(request, 'app/dangnhap.html', context)
def logout_page(request):
    logout(request)
    return redirect('dangnhap')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
        user_not_login = 'hidden'
        user_login = 'show'
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']
        user_not_login = 'show'
        user_login = 'hidden'
    categories = Category.objects.filter(is_sub = False)
    products = Product.objects.all()
    context = {'categories':categories,'products': products, "cartitems": cartitems, "user_not_login": user_not_login, "user_login": user_login}
    return render(request, 'home.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
        user_not_login = 'hidden'
        user_login = 'show'
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']
        user_not_login = 'show'
        user_login = 'hidden'
    context = {'items': items, 'order': order, "cartitems": cartitems,'user_not_login': user_not_login, 'user_login': user_login}
    return render(request , 'app/cart.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
        user_not_login = 'hidden'
        user_login = 'show'
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']
        user_not_login = 'show'
        user_login = 'hidden'
    context = {'items': items, 'order': order, "cartitems": cartitems,'user_not_login': user_not_login, 'user_login': user_login}
    return render(request , 'app/checkout.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    # lay kach hang
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('đã thêm', safe=False)
import datetime
# Lưu địa chỉ 
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        # Kiểm tra tổng tiền gửi từ client có khớp với backend không
        if total == float(order.get_cart_total):
            order.complete = True
        order.save()
        #THÊM ĐOẠN NÀY: Trừ số lượng tồn kho của từng sản phẩm trong đơn
        for item in order.orderitem_set.all():
            product = item.product
            # Nếu sản phẩm có quản lý số lượng tồn kho (giả sử có trường quantity/stock)
            # Bạn điều chỉnh tên trường 'quantity' dưới đây theo đúng Model Product của bạn nhé
            if hasattr(product, 'quantity'): 
                product.quantity -= item.quantity
                if product.quantity < 0:
                    product.quantity = 0
                product.save()

        order.save()
        # Lưu thông tin giao hàng
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            mobile=data['shipping'].get('mobile', ''),
        )
        return JsonResponse('Hoàn tất đặt hàng!', safe=False)
    else:
        return JsonResponse('Tài khoản chưa đăng nhập!', safe=False)
    