from django.http import JsonResponse
from ..models import AddProperty, Room

def api_list_hostels(request):
    hostels = AddProperty.objects.all().values('id', 'hostelname', 'ownername', 'address')
    return JsonResponse(list(hostels), safe=False)

def api_list_rooms(request, property_id):
    rooms = Room.objects.filter(property_id=property_id).values('id', 'room_number', 'floor_type', 'number_of_share', 'available_room_or_not')
    return JsonResponse(list(rooms), safe=False)
