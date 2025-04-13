

# 🛵 Delivery Availability Checker

This Django project allows you to check if a Gomak Delivery agent's location (based on latitude and longitude) falls within the delivery zone of any agent. It supports proximity-based matching using either:

- ✅ Geopy (Haversine formula via `geopy.distance`)
- ✅ Google Maps API (optional, integration-ready – current key not authorized)

## 📦 Features

- Match user’s delivery location using latitude & longitude.
- Return nearest matching delivery zone.
- Show distance and radius of the delivery zone.

## 📥 Installation & Setup

### 1. Clone the Repository


git clone https://github.com/subal75/GoMakDelivery.git

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


🧪 How to Use
✅ API Endpoint

POST: http://127.0.0.1:8000/check-delivery/

Request:

{
    "latitude": 20.2912329,
    "longitude": 85.8549798
}

✅ Sample Response (when delivery available):

{
    "status": true,
    "message": "Delivery available from Rupali Square",
    "agent_location": {
        "location_name": "Rupali Square",
        "radius_km": 20.0,
        "distance_from_user_km": 1.45
    }
}

❌ Sample Response (when delivery not available):

{
  "status": false,
  "message": "No delivery agent available in your area"
}
