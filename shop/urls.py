from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import abuse_cases, api_home, checkout, get_order, home

urlpatterns = [
    path('', home),
    path('abuse-cases/', abuse_cases),
    path('api/', api_home),
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
