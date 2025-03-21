from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription, SubscriptionMember, PaymentTransaction

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = '__all__'

class SubscriptionMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionMember
        fields = '__all__'

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'
