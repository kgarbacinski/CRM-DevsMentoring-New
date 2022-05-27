from django.urls import path

from Payments_system.views import PaymentView

urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
    # path("payment_details/<uuid:payment_id>", payment_details, name='payment-details'),
    # path("payments/", include("payments.urls")),
]