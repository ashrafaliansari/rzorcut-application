from rest_framework import generics
from .models import Store, Appointment
from .serializers import StoreSerializer, AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import EmailOTP
from .serializers import EmailSerializer, OTPVerifySerializer
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.account.views import ConfirmEmailView
from datetime import timedelta, date, datetime
from django.db.models.functions import TruncDate


# Create your views here.
class StoreListView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class StoreAvailabilityView(APIView):
    def get(self, request, store_id):
        try:
            store = Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            return Response({"error": "Store not found"}, status=404)

        start_date = date.today()
        days = [start_date + timedelta(days=i) for i in range(7)]

        # generate time slots
        time_slots = []
        current = store.opening_time
        while current < store.closing_time:
            time_slots.append(current.strftime('%H:%M'))
            current = (datetime.combine(date.today(), current) + timedelta(minutes=60)).time()

        grid = []
        for d in days:
            row = []
            for t in time_slots:
                hour = int(t.split(':')[0])
                is_booked = Appointment.objects.filter(
                    store=store,
                    appointment_time__date=d,
                    appointment_time__hour=hour
                ).exists()
                row.append({
                    "time": t,
                    "booked": is_booked
                })
            grid.append({
                "date": d.strftime("%A, %Y-%m-%d"),
                "slots": row
            })
        return Response({
            "store": store.name,
            "time_slots": time_slots,
            "grid": grid
        })
    
class AppointmentCreateView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            # Optional: prevent double booking
            existing = Appointment.objects.filter(
                store_id=request.data.get('store_id'),
                appointment_time=request.data.get('appointment_time')
            ).exists()
            if existing:
                return Response({"error": "Slot already booked."}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class OwnerAppointmentListView(generics.ListAPIView):
#     serializer_class = AppointmentSerializer

#     def get_queryset(self):
#         store_id = self.request.query_params.get('store_id')
#         if store_id:
#             return Appointment.objects.filter(store_id=store_id)
#         return Appointment.objects.none()

class SendOTPView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            obj, created = EmailOTP.objects.update_or_create(email=email)
            
            # Send OTP to email
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP is: {obj.otp}",
                from_email=None,
                recipient_list=[email],
            )
            return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        print("Received data:", request.data)  #  DEBUG LINE

        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error": "Email and OTP required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_obj = EmailOTP.objects.get(email=email)
            if otp_obj.otp == otp:
                return Response({"valid": True}, status=200)
            else:
                return Response({"error": "Invalid OTP"}, status=400)
        except EmailOTP.DoesNotExist:
            return Response({"error": "OTP not found"}, status=404)
        

class RedirectConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        return redirect('http://localhost:3000/email-confirmed')
    