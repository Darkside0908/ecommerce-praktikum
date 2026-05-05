from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Order

def home(request):
    products = Product.objects.all().order_by("id")
    return render(request, "shop/home.html", {"products": products})

def abuse_cases(request):
    cases = [
        {
            "name": "Checkout without token",
            "attack": "POST /checkout/ tanpa Authorization header",
            "expected": "401 Unauthorized",
            "reason": "Endpoint checkout hanya boleh dipakai user login.",
        },
        {
            "name": "Product ID palsu",
            "attack": "Kirim product_id yang tidak ada di database",
            "expected": "404 Product not found",
            "reason": "Server harus menolak referensi produk invalid.",
        },
        {
            "name": "Quantity bukan angka",
            "attack": "Kirim quantity = 'abc'",
            "expected": "400 Bad Request",
            "reason": "Input harus divalidasi sebelum diproses.",
        },
        {
            "name": "Quantity nol / negatif",
            "attack": "Kirim quantity = 0 atau -1",
            "expected": "400 Bad Request",
            "reason": "Jumlah order harus lebih dari 0.",
        },
        {
            "name": "Order milik user lain",
            "attack": "GET /order/<id>/ untuk order milik akun berbeda",
            "expected": "404 Not found",
            "reason": "User hanya boleh melihat order miliknya sendiri.",
        },
        {
            "name": "Manipulasi harga di client",
            "attack": "Ubah total di request body / browser",
            "expected": "Diabaikan",
            "reason": "Harga dihitung di server, bukan dari client.",
        },
    ]
    return render(request, "shop/abuse_cases.html", {"cases": cases})

@api_view(['GET'])
def api_home(request):
    return Response({
        "message": "Ecommerce API running",
        "endpoints": [
            "GET /",
            "GET /abuse-cases/",
            "POST /login/",
            "POST /api/token/",
            "POST /api/token/refresh/",
            "POST /checkout/",
            "GET /order/<order_id>/",
        ],
    })

# CHECKOUT (SECURE)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity")

    if product_id is None or quantity is None:
        return Response(
            {"error": "product_id and quantity are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return Response(
            {"error": "quantity must be an integer"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if quantity <= 0:
        return Response(
            {"error": "quantity must be greater than 0"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # SERVER-SIDE PRICE
    total = product.price * quantity

    order = Order.objects.create(
        user=request.user,
        product=product,
        quantity=quantity,
        total=total
    )

    return Response({
        "order_id": order.id,
        "total": total
    })

# GET ORDER (SECURE)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        return Response({
            "product": order.product.name,
            "total": order.total
        })
    except Order.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

# Create your views here.
