from rest_framework.viewsets import ModelViewSet
from .models import SubscriptionPlan, UserSubscription, SubscriptionMember, PaymentTransaction
from .serializers import (
    SubscriptionPlanSerializer, UserSubscriptionSerializer, 
    SubscriptionMemberSerializer, PaymentTransactionSerializer
)

class SubscriptionPlanViewSet(ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

class UserSubscriptionViewSet(ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer

class SubscriptionMemberViewSet(ModelViewSet):
    queryset = SubscriptionMember.objects.all()
    serializer_class = SubscriptionMemberSerializer

class PaymentTransactionViewSet(ModelViewSet):
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
