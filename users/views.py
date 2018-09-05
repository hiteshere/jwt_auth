from django.contrib.auth.signals import user_logged_in
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
from twilio.rest import Client
from jwt_auth import settings
from .serializers import UserSerializer, JobSerializer
from .models import User, Job


class CreateUserAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        otp_check(serializer.data['id'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)
        # serializer.data.__setitem__("email", request.user.email)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class JobRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = JobSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        qs = Job.objects.filter(user=request.user)
        serializer = self.serializer_class(qs[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class OtpCheckAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    permission_classes = (permissions.AllowAny,)
    serializer_class = JobSerializer

    def post(self, request, *args, **kwargs):
        if int(request.data['otp']) in list(User.objects.all().values_list('id', flat=True)):
            return Response(request.data, status=status.HTTP_200_OK)
        return Response(request.data, status=status.HTTP_404_NOT_FOUND)


def otp_check(user_id):
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = 'AC53ea4d8ea0a6156709fb404a3c2a49f2'
    auth_token = '5f9c52b90ebe13c9029d44ac8875e095'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+17653003821',
        body=user_id,
        to='+918076786402'
    )

@api_view(['POST'])
# @permission_classes([permissions.AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email, password=password)
        if user:
            user = user.first()
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                user_details['email'] = user.email
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                print(user_details)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'User with given credentials does not exists.'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)



