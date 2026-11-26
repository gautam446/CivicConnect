from django.core.management.base import BaseCommand
from complaints.models import Category
from rewards.models import Reward

class Command(BaseCommand):
    help = "Create starter categories and rewards"
    def handle(self, *args, **options):
        for name, desc in [
            ("Road", "Potholes, damaged roads and footpaths"),
            ("Water", "Water leakage and supply issues"),
            ("Garbage", "Waste collection and cleanliness"),
            ("Electricity", "Street lights and public electricity"),
            ("Drainage", "Blocked drains and overflow"),
            ("Other", "Other civic issues"),
        ]:
            Category.objects.get_or_create(name=name, defaults={"description": desc})
        for title, desc, points in [
            ("₹50 Shopping Coupon", "Demo coupon; vendor partnership required.", 500),
            ("₹100 Shopping Coupon", "Demo coupon; vendor partnership required.", 900),
            ("Food Discount Coupon", "Demo coupon; vendor partnership required.", 400),
            ("Movie Discount Coupon", "Demo coupon; vendor partnership required.", 700),
        ]:
            Reward.objects.get_or_create(title=title, defaults={"description": desc, "points_required": points})
        self.stdout.write(self.style.SUCCESS("Starter categories and rewards created."))
