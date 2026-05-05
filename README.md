# E-Commerce API + Frontend (Django + DRF + JWT)

API + frontend sederhana untuk login, checkout, lihat order, dan demo abuse cases.

## Requirements

- Python 3.13 (atau minimal 3.10+)
- Django 6.x
- djangorestframework
- djangorestframework-simplejwt

## Cara Menjalankan

Masuk ke folder project yang ada `manage.py`:

```bash
cd ecommerce
```

Install dependency:

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

Buat migration + apply ke database:

```bash
python manage.py makemigrations shop
python manage.py migrate
```

Buat user login:

```bash
python manage.py createsuperuser
```

Jalankan server:

```bash
python manage.py runserver
```

Base URL: `http://127.0.0.1:8000`

## Endpoint

- `GET /` - frontend utama
- `GET /abuse-cases/` - daftar abuse cases
- `GET /api/` - info API
- `POST /login` atau `POST /login/` - ambil JWT token
- `POST /api/token` atau `POST /api/token/` - ambil JWT token
- `POST /api/token/refresh` atau `POST /api/token/refresh/` - refresh token
- `POST /checkout` atau `POST /checkout/` - buat order (butuh access token)
- `GET /order/<order_id>/` - lihat order milik user login (butuh access token)

## Alur Test di Postman

1. Login dulu:

```http
POST http://127.0.0.1:8000/login/
Content-Type: application/json

{
  "username": "username_kamu",
  "password": "password_kamu"
}
```

Respons berisi:
- `access` -> dipakai untuk Authorization
- `refresh` -> dipakai untuk refresh token

2. Tambah 1 produk dulu (wajib), contoh cepat via shell:

```bash
python manage.py shell -c "from shop.models import Product; p=Product.objects.create(name='Laptop', price=15000000); print(p.id)"
```

3. Checkout:

```http
POST http://127.0.0.1:8000/checkout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```

Contoh response:

```json
{
  "order_id": 1,
  "total": 30000000
}
```

4. Cek order:

```http
GET http://127.0.0.1:8000/order/1/
Authorization: Bearer <access_token>
```

## Alur Pakai Frontend

1. Buka `http://127.0.0.1:8000/`
2. Login pakai username/password Django
3. Pilih produk dan checkout
4. Lihat hasil order di panel output
5. Buka `http://127.0.0.1:8000/abuse-cases/` untuk melihat skenario penyalahgunaan

## Error Umum

- `401 Authentication credentials were not provided`
  - Header `Authorization: Bearer <access_token>` belum dikirim.

- `OperationalError: no such table: shop_product`
  - Belum `makemigrations` / `migrate`.

- `Product matching query does not exist`
  - `product_id` belum ada di database.

## Abuse Cases yang Ditampilkan

- Checkout tanpa token
- Product ID palsu
- Quantity bukan angka
- Quantity nol / negatif
- Akses order milik user lain
- Manipulasi harga di client
