from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins, generics
from rest_framework import status

from django.utils.crypto import get_random_string
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from rest_framework_jwt.settings import api_settings

from .models import Booking, Property, User
from .serializers import PropertyBookingsSerializer, UserBookingsSerializer, BookingSerializer


class PropertyBookingsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PropertyBookingsSerializer
    permission_classes = ()

    def get_queryset(self):
        property = get_object_or_404(Property, property_id=self.kwargs['property_id'])
        return Booking.objects.filter(property=property)


class UserBookingsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserBookingsSerializer
    permission_classes = ()

    def get_queryset(self):
        user = get_object_or_404(User, uuid=self.kwargs['user_id'])
        return Booking.objects.filter(user=user)


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer


class Registration(APIView):
    permission_classes = ()
    
    def create_user(self, username, request):                
        password = get_random_string()
        email = get_random_string() + '@co.co'  
        try:               
            user = User.objects.create_user(username, email, password)
        except:  # user already exists
            user = User.objects.get(username=username)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return user
    
    def get_token(self, user):
        payload = api_settings.JWT_PAYLOAD_HANDLER(user)
        token = api_settings.JWT_ENCODE_HANDLER(payload)
        return token

    def post(self, request):
        user = self.create_user(request.data['username'], request)
        token = self.get_token(user)
        return Response({'token': token, 'user_id': user.uuid}, status=status.HTTP_201_CREATED)
