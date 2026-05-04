from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Order

@api_view(['GET'])
def api_home(request):
    return Response({
        "message": "Ecommerce API running",
        "endpoints": [
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
    quantity = int(request.data.get("quantity"))

    product = Product.objects.get(id=product_id)

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
    except:
        return Response({"error": "Not found"}, status=404)

# Create your views here.
