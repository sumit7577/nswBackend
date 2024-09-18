from django.shortcuts import render
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
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
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from rest_framework.generics import CreateAPIView,UpdateAPIView,GenericAPIView
from rest_framework.parsers import MultiPartParser


# Create your views here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class RegisterUserView(CreateAPIView):
      serializer_class = RegisterUserSerializer

      def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the validated data (creates Otp and sends email)
            return Response({"status": True, "message": "OTP sent to your email."}, status=status.HTTP_201_CREATED)
        
        return Response({"status": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class OtpVerifyView(CreateAPIView):
    serializer_class = OtpSerializer

    def create(self, request, *args, **kwargs):
        # Initialize the serializer with the request data
        serializer = self.get_serializer(data=request.data)
        
        # Validate the serializer
        if not serializer.is_valid():
            return Response({"status": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        otp_value = serializer.validated_data.get("otp")
        
        try:
            otp_instance = Otp.objects.filter(otp=otp_value).latest('created_at')
        except Otp.DoesNotExist:
            return Response({"status": False, "errors": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the user
        user = CustomUser.objects.create_user(
            email=otp_instance.email,
            password=otp_instance.password,  # Ensure this is already hashed
            phone=otp_instance.phone
        )
        user_data = UserDetailSerialzer(user)
        token, _ = Token.objects.get_or_create(user=user)
        
        # Optionally delete the OTP instance or mark it as used
        otp_instance.delete()
        
        return Response({"status": True, "user": user_data.data,"token":token.key}, status=status.HTTP_201_CREATED)

    
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
    


class CourseView(ModelViewSet):
    pagination_class = AppPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    


class SingleCourseView(ReadOnlyModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get("pk"))
    
    def check_user(self,request,*args,**kwargs):
        paid = False
        course = Course.objects.prefetch_related("students").filter(students=request.user,id=kwargs.get("pk"))
        if len(course) > 0:
            self.serializer_class = SingleCourseSerializerPaid
            paid = True
        return paid
    
    def getInstallment(self,paid:bool):
        data = Installment.objects.filter(course= self.kwargs.get("pk"))
        serialized_data = InstallmentSerializer(data,many=True)
        if paid:
            serialized_data = PaidInstallmentSerializer(data,many=True)
        return serialized_data.data

    def retrieve(self, request, *args, **kwargs):
        data  = self.check_user(request=request,*args,**kwargs)
        installment = self.getInstallment(data)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = {"paid":data,"data":serializer.data,'installment':installment}
        return Response(response)
    


class Checkout(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    def get(self,request,pk):
        course = Course.objects.filter(id=pk)
        userRegistered = Course.objects.filter(id=pk,students=request.user.id)
        if len(userRegistered) > 0:
            return Response({"success":False,"message":"Course Already Purchased!"},status=400)
        if len(course) > 0:
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            order = client.order.create({'amount': course[0].registration_fees*100, 'currency': 'INR'})
            local_order = Order.objects.create(course=course[0],user=request.user,order_data=order)
            context = {"key":settings.RAZORPAY_API_KEY,"order":order,"course":course[0],"id":local_order.id,"host": request.get_host()  }
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
                Course.objects.get(id=order.course.id).students.add(order.user)
                return Response({"success": True, "message": "Payment Completed Succesfull!"}, status=200)
        except Exception as e:
            print(e)
            return Response({"success": False, "message": "Payment Not Completed!"}, status=400)




def check_signature(order_id:str,payment_id:str,signature:str):
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    verify = client.utility.verify_payment_signature({'razorpay_order_id': order_id,'razorpay_payment_id': payment_id,
                                             'razorpay_signature': signature})
    return verify


class Orders(ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user,status="SUCCESS")
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)



class UpdateOwnProfile(GenericAPIView):
    serializer_class = UpdateUserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user

    def patch(self, request, *args, **kwargs):
        # Get the current user object
        user = self.get_object()

        # Pass the request data to the serializer
        serializer = self.get_serializer(user, data=request.data, partial=True)

        # Check if the data is valid
        if serializer.is_valid():
            serializer.save()  # Save the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)