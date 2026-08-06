#!/usr/bin/env bash
# Exit on error
set -o errexit
#Cài đặt các thư viện cần thiết (Django, PostgreSQL vân vân) lên server Render.
pip install -r requirements.txt 
# Gom các file giao diện (CSS, JS) để trang web và trang Admin không bị vỡ.
python manage.py collectstatic --no-input
# Chạy các lệnh migrate để tạo các bảng trong cơ sở dữ liệu.
python manage.py migrate
# Tạo tài khoản Admin để đăng nhập vào trang Admin của Django. Nếu tài khoản đã tồn tại thì bỏ qua lỗi.
python manage.py createsuperuser --noinput || true