import secrets, string
from django.db import transaction
from django.db.models import Sum, Q
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Reward, RewardTransaction, Redemption
from .serializers import RewardSerializer, TransactionSerializer, RedemptionSerializer

def balance_for(user):
    earned = RewardTransaction.objects.filter(user=user, transaction_type="earned").aggregate(v=Sum("points"))["v"] or 0
    spent = RewardTransaction.objects.filter(user=user, transaction_type="redeemed").aggregate(v=Sum("points"))["v"] or 0
    return earned - spent

class RewardListView(generics.ListAPIView):
    queryset = Reward.objects.filter(active=True).order_by("points_required")
    serializer_class = RewardSerializer
    permission_classes = [permissions.IsAuthenticated]

class MyRewardsView(APIView):
    def get(self, request):
        tx = RewardTransaction.objects.filter(user=request.user).order_by("-created_at")
        redemptions = Redemption.objects.filter(user=request.user).order_by("-redeemed_at")
        return Response({
            "balance": balance_for(request.user),
            "transactions": TransactionSerializer(tx, many=True).data,
            "redemptions": RedemptionSerializer(redemptions, many=True).data,
        })

class RedeemView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            reward = Reward.objects.select_for_update().get(pk=request.data.get("reward_id"), active=True)
        except (Reward.DoesNotExist, ValueError, TypeError):
            return Response({"detail": "Reward not found."}, status=404)
        user = request.user
        if user.role != "citizen":
            return Response({"detail": "Only citizens can redeem rewards."}, status=403)
        if balance_for(user) < reward.points_required:
            return Response({"detail": "Not enough points."}, status=400)
        RewardTransaction.objects.create(user=user, points=reward.points_required,
            transaction_type="redeemed", description=f"Redeemed: {reward.title}")
        alphabet = string.ascii_uppercase + string.digits
        code = "CIV-" + "".join(secrets.choice(alphabet) for _ in range(10))
        redemption = Redemption.objects.create(user=user, reward=reward, coupon_code=code)
        return Response({"message": "Reward redeemed.", "redemption": RedemptionSerializer(redemption).data,
                         "balance": balance_for(user)}, status=201)

class LeaderboardView(APIView):
    def get(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = User.objects.filter(role="citizen", is_active=True)
        rows = []
        for user in users:
            points = balance_for(user)
            if points > 0:
                rows.append({"username": user.username, "points": points})
        rows.sort(key=lambda x: x["points"], reverse=True)
        return Response(rows[:20])
