from django.urls import path
from . import views
from .views import SendOTPView, VerifyOTPView, RedirectConfirmEmailView, StoreAvailabilityView,AppointmentCreateView

urlpatterns = [
    path('stores/', views.StoreListView.as_view()),
    # path('availability/', views.AvailabilityView.as_view()),
    # path('appointments/', views.AppointmentListCreateView.as_view()),
    # path('owner/appointments/', views.OwnerAppointmentListView.as_view()),
    # path('appointments/<int:pk>/', views.AppointmentDetailView.as_view()),
    # new paths
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('api/auth/registration/account-confirm-email/<str:key>/', RedirectConfirmEmailView.as_view(), name='account_confirm_email'),
    path("api/auth/registration/account-confirm-email/<str:key>/",RedirectConfirmEmailView.as_view(),name="account_confirm_email"),
    path('store/<int:store_id>/availability/', StoreAvailabilityView.as_view(),name='store-availability'),
    path('appointments/', AppointmentCreateView.as_view(), name='create-appointment'),

]
