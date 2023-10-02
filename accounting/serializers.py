from rest_framework.serializers import ModelSerializer
from .models import PaymentCredentials

class PaymentCredentialsSerializer(ModelSerializer):
    class Meta:
        model = PaymentCredentials
        fields = '__all__'