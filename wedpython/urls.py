"""
URL configuration for wedpython project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from app import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.http import HttpResponse
from django.contrib.auth import get_user_model
 
# Hàm tạo admin tự động chạy qua trình duyệt
def create_admin_view(request):
    User = get_user_model()
    user, _ = User.objects.get_or_create(username='admin')
    user.set_password('123456')
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    return HttpResponse("<h1>TAO ADMIN THANH CONG! Mat khau: 123456</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('fix-admin/', create_admin_view),
    path('', include('app.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^images/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
