from django.urls import path
from . import views

urlpatterns = [
    path('stores/', views.StoreListView.as_view()),
    path('availability/', views.AvailabilityView.as_view()),
    path('appointments/', views.AppointmentListCreateView.as_view()),
    path('owner/appointments/', views.OwnerAppointmentListView.as_view()),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view()),
]
