# from math import radians, sin, cos, sqrt, atan2
#
#
# def haversine(lat1, lon1, lat2, lon2):
#     """
#     Calculate the great-circle distance between two points
#     on the Earth (specified in decimal degrees)
#     """
#     # Convert decimal degrees to radians
#     lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
#
#     # Haversine formula
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))
#     r = 6371  # Radius of Earth in kilometers
#     return c * r
#
#
# from django.db.models import Q
#
#
# def check_agent_availability(delivery_address):
#     """
#     Check if any GomakDelivery agent is available for the given address
#     Returns queryset of available agents
#     """
#     # First check by pincode (exact match)
#     agents = GomakDelivery.objects.filter(pincode=delivery_address.pincode)
#
#     # If no agents found by pincode, check by distance
#     if not agents.exists():
#         agents = GomakDelivery.objects.filter(
#             Q(latitude__isnull=False) &
#             Q(longitude__isnull=False)
#         )
#
#         available_agents = []
#         for agent in agents:
#             distance = haversine(
#                 agent.latitude, agent.longitude,
#                 delivery_address.latitude, delivery_address.longitude
#             )
#             if distance <= agent.radius:
#                 available_agents.append(agent.id)
#
#         agents = GomakDelivery.objects.filter(id__in=available_agents)
#
#     return agents