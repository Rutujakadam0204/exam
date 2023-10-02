from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.db import transaction
from django.utils.http import urlsafe_base64_decode
from .models import CollegeRegistration, Invoice, PaymentCredentials, PackageSetting, Profile
from .serializers import PaymentCredentialsSerializer
from .tasks import disable_student_group
from random import randint
import logging
import traceback
import hashlib
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class PaymentCredentialsView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'payment_setting.html'

    @transaction.atomic()
    def get(self, request):
        if request.user.is_superuser:
            data = {}
            if PackageSetting.objects.all().count() > 0 :
                    data['package_setting'] = PackageSetting.objects.all().latest('id')
            if PackageSetting.objects.all().count() > 0:
                    data['payment_credentials'] = PaymentCredentials.objects.all().latest('id')
            return Response(data)
        else:
            return redirect('/')
        
    @transaction.atomic()
    def post(self, request, request_type):
        if request.user.is_superuser:
            data = {}
            if request_type == 'payment_settings':
                
                if len(PaymentCredentials.objects.all()) == 1:
                    payment_cred = PaymentCredentials.objects.all().latest('id')
                    payment_serializer = PaymentCredentialsSerializer(payment_cred, data=request.data)
                    data['message'] = "Payment credentails edited successfully."

                else:
                    payment_serializer = PaymentCredentialsSerializer(data=request.data)
                    data['message'] = "Payment credentails saved successfully."
                if payment_serializer.is_valid():    
                    payment_serializer.save()
            else:
                if len(PackageSetting.objects.all()) == 1:
                    package_setting = PackageSetting.objects.all().latest('id')
                    package_setting.price_per_student = request.data['price_per_student']
                    data['message'] = "Payment credentails edited successfully."

                else:
                    package_setting = PackageSetting.objects.create(price_per_student=request.data['price_per_student'])
                    data['message'] = "Payment credentails saved successfully."
                package_setting.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return redirect('/')


def paymentview(request, token):
    if request.method == "GET":
        data = {}
        college_email = urlsafe_base64_decode(token)
        college_email = college_email.decode('UTF-8')
        
        if CollegeRegistration.objects.filter(college_email=college_email, payment=True).exists():
            return redirect('/accouning/payment-history')
        else:
            college = CollegeRegistration.objects.get(college_email=college_email, payment=False)
            package_setting = PackageSetting.objects.all().latest('id')
            student_limit = college.student_limit
            amount = student_limit * package_setting.price_per_student
            # code for payment
            context = {}
            pay_set = PaymentCredentials.objects.all().latest('id')
            key = pay_set.secret_key
            amt = str(amount)
            name = college.college_name
            email = college.college_email
            salt = pay_set.secret_id
            txnid = get_transaction_id()
            hash_ = generate_hash(request, key=key, txnid=txnid, amt=amt, name=name, email=email, salt=salt)
            hash_string = get_hash_string(request, key=key, txnid=txnid, amt=amt, name=name, email=email, salt=salt)
            # use constants file to store constant values.
            # use test URL for testing
            context["action"] = 'https://secure.payu.in/_payment'
            context["amount"] = amount
            context["productinfo"] = "Message showing product details."
            context["key"] = pay_set.secret_key
            context["txnid"] = txnid
            context["hash"] = hash_
            context["hash_string"] = hash_string
            context["firstname"] = college.college_name
            context["email"] = college.college_email
            context["phone"] = college.mobile_number
            context["service_provider"] = "payu_paisa"
            context['payment_gateway'] = 'payu'
            context["furl"] = '/accounting/payment_handler/fail/' + token
            context["surl"] = '/accounting/payment_handler/pass/' + token
        return render(request, 'payment.html', context)
    
@csrf_exempt
def payment_handler(request, status, token):
    data = {}
    if status == 'fail':
        data['message'] = "Payment Failed."
    else:
        college_email = urlsafe_base64_decode(token)
        college_email = college_email.decode('UTF-8')
        college = CollegeRegistration.objects.get(college_email=college_email, payment=False)
        college.payment = True
        college.save()
        Profile.objects.filter(college=college, user__groups__name='student').update(login_allow=True)

        disable_student_group.apply_async(args=[college_email], countdown=31536000)
        
        data['message'] = "Payment Successfull."
    return render(request, 'payment_status.html', data)


class PaymentHistoryView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'invoice.html'

    @transaction.atomic()
    def get(self, request):
        data = {
            'invoice': Invoice.objects.filter(college__id=request.user.profile.college.id)
        }
        return Response(data)
    
"""Generate hash for payumoney"""


def generate_hash(request, key, txnid, amt, name, email, salt):
    try:
        # get keys and SALT from dashboard once account is created.
        hash_string = get_hash_string(request, key=key, txnid=txnid, amt=amt, name=name, email=email, salt=salt)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return generated_hash
    except Exception:
        # log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


"""create hash string using all the fields"""


def get_hash_string(request, key, txnid, amt, name, email, salt):
    hash_string = key + "|" + txnid + "|" + amt + "|" + "Message showing product details." + "|"
    hash_string += name + "|" + email + "|"
    hash_string += "||||||||||" + salt

    return hash_string


"""generate a random transaction Id for PayU money."""


def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0, 9999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid