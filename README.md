# CivicConnect — Smart Community & Reward Management System

A runnable starter project with:
- Django + Django REST Framework backend
- PostgreSQL database (configured through `.env`)
- React + Vite frontend
- JWT authentication
- Citizen, staff and admin roles
- Complaint creation, tracking, status updates and staff assignment
- Reward points, reward catalogue and redemption
- Django admin panel

> This is a complete MVP foundation, not a live municipal service. Real coupons require partnerships and manual fulfilment. Configure email and production security before public launch.

## Requirements
- Python 3.10+
- PostgreSQL 14+
- Node.js 18+
- npm

## 1. Create PostgreSQL database
Open pgAdmin or psql and run:

```sql
CREATE DATABASE civicconnect;
```

## 2. Backend setup (Windows CMD)
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```
Edit `backend/.env` and set your PostgreSQL username/password.

Run migrations and create starter categories/rewards:
```cmd
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

Backend: http://127.0.0.1:8000  
Django admin: http://127.0.0.1:8000/admin/  
API root: http://127.0.0.1:8000/api/

## 3. Frontend setup (second CMD window)
```cmd
cd frontend
npm install
copy .env.example .env
npm run dev
```
Frontend: http://localhost:5173

## Demo flow
1. Register a citizen account from the frontend.
2. Log in and create a complaint with category, description and location.
3. Log in to Django admin and mark the complaint as `verified` to award points.
4. Change status to `in_progress` or `resolved` as work progresses.
5. Add staff accounts using Django admin; assign staff from the complaint admin.
6. Seeded rewards appear in the Rewards section. A citizen can redeem if they have enough points.

## Roles
- `citizen`: can create and view their own complaints and redeem rewards.
- `staff`: can view complaints assigned to them and update their assigned complaint status.
- `admin`: use Django admin for full management. Create admin users with `is_staff=True` or via createsuperuser.

## Important implementation notes
- Points are credited once when an admin changes a complaint to `verified`.
- A complaint is not automatically considered solved merely because it was submitted.
- Coupon codes in this MVP are generated placeholders. Connect real vendors before offering actual discounts.
- For production, add HTTPS, secure secret management, rate limiting, audit logging, backups, email/SMS provider and stronger moderation.
