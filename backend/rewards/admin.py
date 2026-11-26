from django.contrib import admin
from .models import Reward, RewardTransaction, Redemption
admin.site.register(Reward)
admin.site.register(RewardTransaction)
admin.site.register(Redemption)
