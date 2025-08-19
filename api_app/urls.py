from django.urls import path
from .views import UserRegister,ProductsModelView,Orders,OrderDetail
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.routers import DefaultRouter


#/api/
urlpatterns = [
    path('register', UserRegister.as_view(), name='register'),
    path('token', TokenObtainPairView.as_view(), name='token_login'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('order', Orders.as_view(), name='list_order'),
    path('order/<int:pk>', OrderDetail.as_view(), name='order_detail'),

]
router = DefaultRouter()
router.register(r'product', ProductsModelView, basename='product')
urlpatterns += router.urls