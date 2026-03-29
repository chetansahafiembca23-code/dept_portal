from django.urls import path
from .views import (
    event_list, 
    event_detail, 
    enroll_activity, 
    enrollment_success, 
    download_receipt, 
    export_enrollments_csv,
    payment_verify  # <--- MAKE SURE THIS IS HERE
)

urlpatterns = [
    path('', event_list, name='event_list'),
    path('<int:event_id>/', event_detail, name='event_detail'),
    path('enroll/<int:activity_id>/', enroll_activity, name='enroll_activity'),
    path('success/<int:enrollment_id>/', enrollment_success, name='enrollment_success'),
    path('receipt/<int:enrollment_id>/', download_receipt, name='download_receipt'),
    path('export/<int:event_id>/', export_enrollments_csv, name='export_enrollments'),
    path('payment/verify/', payment_verify, name='payment_verify'),
]