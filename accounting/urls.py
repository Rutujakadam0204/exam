from .views import paymentview,payment_handler, PaymentHistoryView, PaymentCredentialsView
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path('payment-setting', login_required(PaymentCredentialsView.as_view()), name='payment-setting'),

    path('payment-setting/<request_type>', login_required(PaymentCredentialsView.as_view()), name='payment-setting'),

    path('payment-after-invoice/<token>', paymentview, name='payment'),

    path('payment-history', login_required(PaymentHistoryView.as_view()), name='payment-history'),

    path('payment_handler/<status>/<token>', payment_handler, name='payment_handler')

]