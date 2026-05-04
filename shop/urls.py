from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import api_home, checkout, get_order

urlpatterns = [
    path('', api_home),
    path('login', TokenObtainPairView.as_view(), name='login_no_slash'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair_no_slash'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh_no_slash'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('checkout', checkout, name='checkout_no_slash'),
    path('checkout/', checkout),
    path('order/<int:order_id>/', get_order),
]
