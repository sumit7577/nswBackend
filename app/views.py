from django.shortcuts import render
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from app.models import *
from app.serializers import *
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
import razorpay
from app.paginator import AppPagination

# Create your views here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class RegisterUserView(ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()
 
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

class LoginView(APIView):
    """Login The User Using Auth Token"""
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.get(username=request.data["username"])
                hashedPassword = user.password
                password = check_password(
                    request.data["password"], hashedPassword)
                if password:
                    token = Token.objects.get_or_create(user=user)
                    serializers = UserDetailSerialzer(user, many=False)
                    return Response({"success": True, "token": token[0].key,"user":serializers.data}, status=200)
                return Response({"success": False, "message": "Username Or Password Incorrect"}, status=400)
            except Exception as e:
                return Response({"success": False, "message": "Username Or Password Incorrect"}, status=400)
        return Response(serializer.errors, status=400)
    


class Checkout(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    def get(self,request,pk):
        course = Course.objects.filter(id=pk)
        if len(course) > 0:
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            order = client.order.create({'amount': course[0].price*100, 'currency': 'INR'})
            local_order = Order.objects.create(course=course[0],user=request.user,order_data=order)
            context = {"key":settings.RAZORPAY_API_KEY,"order":order,"course":course[0],"id":local_order.id}
            return render(request=request,template_name="order.html",context=context)
        else:
            return Response({"success":False,"message":"Course Not Found!"},status=400)



class CheckoutSuccess(APIView):
    def post(self,request):
        payment_id = request.data.get("payment_id")
        order_id = request.data.get("order_id")
        signature = request.data.get("signature")
        try:
            signature_hash = check_signature(order_id,payment_id,signature)
            if signature_hash:
                order = Order.objects.get(order_data__id=order_id)
                order.status = "SUCCESS"
                order.payment_id = payment_id
                order.order_id = order_id
                order.signature = signature
                order.save()
                course = Course.objects.get(id=order.course.id).students.add(order.user)
                course.save()
                return render(request=request,template_name="success.html")
        except Exception as e:
            return render(request=request,template_name="success.html")


def check_signature(order_id:str,payment_id:str,signature:str):
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    verify = client.utility.verify_payment_signature({'razorpay_order_id': order_id,'razorpay_payment_id': payment_id,
                                             'razorpay_signature': signature})
    return verify