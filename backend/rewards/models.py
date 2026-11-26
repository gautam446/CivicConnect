from django.conf import settings
from django.db import models

class RewardTransaction(models.Model):
    TYPES = (("earned", "Earned"), ("redeemed", "Redeemed"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reward_transactions")
    points = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, choices=TYPES)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.user} {self.transaction_type} {self.points}"

class Reward(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    points_required = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    def __str__(self): return self.title

class Redemption(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="redemptions")
    reward = models.ForeignKey(Reward, on_delete=models.PROTECT)
    coupon_code = models.CharField(max_length=30, unique=True)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    def __str__(self): return f"{self.user} - {self.reward}"
