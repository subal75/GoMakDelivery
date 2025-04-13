import requests
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from geopy.distance import geodesic
from .models import GomakDelivery


@method_decorator(csrf_exempt, name='dispatch')
class CheckDeliveryAvailabilityView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            lat = data.get('latitude')
            lon = data.get('longitude')

            if lat is None or lon is None:
                return JsonResponse({'status': False, 'message': 'Latitude and longitude are required'}, status=400)

            customer_location = (lat, lon)
            agents = GomakDelivery.objects.all()

            matching_agents = []

            for agent in agents:
                agent_location = (agent.latitude, agent.longitude)

                distance_km = geodesic(customer_location, agent_location).km

                if distance_km <= agent.radius_km:
                    matching_agents.append({
                        'agent': agent,
                        'distance_km': distance_km
                    })

            if not matching_agents:
                return JsonResponse({'status': False, 'message': 'No delivery agent available in your area'})

            # Get agent with minimum distance
            nearest = min(matching_agents, key=lambda x: x['distance_km'])
            agent = nearest['agent']
            distance_km = nearest['distance_km']

            return JsonResponse({
                'status': True,
                'message': f"Delivery available from {agent.location_name}",
                'agent_location': {
                    'location_name': agent.location_name,
                    'radius_km': round(agent.radius_km, 2),
                    'distance_from_user_km': round(distance_km, 2)
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': False, 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)}, status=500)


GOOGLE_API_KEY = 'AIzaSyBNZ6QvXiknFj5OmY4hnUxPoWDnmtQiLko'


@method_decorator(csrf_exempt, name='dispatch')
class CheckDeliveryWithGoogleAPI(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            lat = data.get('latitude')
            lon = data.get('longitude')

            if lat is None or lon is None:
                return JsonResponse({'status': False, 'message': 'Latitude and longitude are required'}, status=400)

            customer_location = (lat, lon)

            # Optional: get formatted address using Google API
            geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={GOOGLE_API_KEY}"

            geo_response = requests.get(geo_url)
            print('geo response: ', geo_response)
            geo_data = geo_response.json()
            print('geo data: ', geo_data)

            if geo_data['status'] != 'OK':
                formatted_address = "Unknown Location"
            else:
                formatted_address = geo_data['results'][0]['formatted_address']

            # Check all agents
            agents = GomakDelivery.objects.all()
            matching_agents = []

            for agent in agents:
                agent_location = (agent.latitude, agent.longitude)
                distance_km = geodesic(customer_location, agent_location).km

                if distance_km <= agent.radius_km:
                    matching_agents.append({
                        'agent': agent,
                        'distance_km': distance_km
                    })

            if not matching_agents:
                return JsonResponse({
                    'status': False,
                    'message': 'No delivery agent available in your area',
                    'user_location': formatted_address
                })

            # Nearest agent within radius
            nearest = min(matching_agents, key=lambda x: x['distance_km'])
            agent = nearest['agent']
            distance_km = nearest['distance_km']

            return JsonResponse({
                'status': True,
                'message': f"Delivery available from {agent.location_name}",
                'user_location': formatted_address,
                'agent_location': {
                    'location_name': agent.location_name,
                    'radius_km': round(agent.radius_km, 2),
                    'distance_from_user_km': round(distance_km, 2)
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': False, 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)}, status=500)
