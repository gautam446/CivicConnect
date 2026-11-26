from rest_framework import serializers
from .models import Reward, RewardTransaction, Redemption

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardTransaction
        fields = "__all__"

class RedemptionSerializer(serializers.ModelSerializer):
    reward_title = serializers.CharField(source="reward.title", read_only=True)
    class Meta:
        model = Redemption
        fields = ("id", "reward", "reward_title", "coupon_code", "redeemed_at", "used")
