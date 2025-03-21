from django.db import models
from apps.core.models import BaseModel  # Import BaseModel từ core

class SubscriptionPlan(BaseModel):
    """Model for subscription plans"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=dict)  # Requires PostgreSQL
    # max_devices = models.IntegerField(default=1)
    max_users = models.IntegerField(default=1)    
    
    
    def __str__(self):
        return self.name


class UserSubscription(BaseModel):
    """Model for user subscriptions"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('paused', 'Paused'),
    ]
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='user_subscriptions')
    address = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    auto_renew = models.BooleanField(default=True)
    payment_method = models.CharField(max_length=100)  # zalopay, vnpay, etc.
    subscription_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    trial_period = models.BooleanField(default=False)
    last_billing_date = models.DateField(null=True, blank=True)
    next_billing_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.plan} ({self.subscription_status})"
    
    
class SubscriptionMember(BaseModel):
    """Model for members of a subscription"""
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='membership')
    address = models.CharField(max_length=255, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('subscription', 'user')
        
    def __str__(self):
        return f"{self.user} member of {self.subscription}"
    
    
class PaymentTransaction(BaseModel):
    """Model for payment transactions"""
    PAYMENT_STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('pending', 'Pending'),
    ]
    
    TRANSACTION_TYPE_CHOICES = [
        ('subscription', 'Subscription'),
        ('one-time', 'One-time'),
    ]
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='payment_transactions')
    subscription = models.ForeignKey(UserSubscription, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)  # zalopay, vnpay, etc.
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='completed')
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE_CHOICES, default='subscription')
    invoice_id = models.CharField(max_length=100, blank=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.user} - {self.amount} {self.currency} ({self.payment_status})"