from django.urls import path
from .views import RewardListView, MyRewardsView, RedeemView, LeaderboardView
urlpatterns = [
    path("rewards/", RewardListView.as_view()),
    path("rewards/me/", MyRewardsView.as_view()),
    path("rewards/redeem/", RedeemView.as_view()),
    path("leaderboard/", LeaderboardView.as_view()),
]
