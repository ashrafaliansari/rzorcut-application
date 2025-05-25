from rest_framework import generics
from .models import Store, Appointment
from .serializers import StoreSerializer, AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response




# Create your views here.
class StoreListView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class AvailabilityView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Availability check coming soon."})
class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class OwnerAppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        store_id = self.request.query_params.get('store_id')
        if store_id:
            return Appointment.objects.filter(store_id=store_id)
        return Appointment.objects.none()