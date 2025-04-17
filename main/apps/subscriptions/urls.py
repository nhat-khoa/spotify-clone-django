from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubscriptionPlanViewSet, UserSubscriptionViewSet, 
    SubscriptionMemberViewSet, PaymentTransactionViewSet
)
from .payment_views import create_payment, zalopay_callback, order_status

router = DefaultRouter()
router.register(r'subscription-plans', SubscriptionPlanViewSet, basename='subscription-plan')
router.register(r'user-subscriptions', UserSubscriptionViewSet, basename='user-subscription')
router.register(r'subscription-members', SubscriptionMemberViewSet, basename='subscription-member')
router.register(r'payment-transactions', PaymentTransactionViewSet, basename='payment-transaction')

urlpatterns = [
    path('', include(router.urls)),

    path('payment/create/', create_payment, name='create-payment'),
    path('payment/callback/', zalopay_callback, name='callback'),
    path('payment/status/', order_status, name='status'),
]
