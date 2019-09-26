from django.conf.urls import url, include
from .views import PropertyBookingsViewSet, UserBookingsViewSet, BookingCreateView, Registration

from rest_framework import routers


router = routers.SimpleRouter()

router.register(
    r'properties/(?P<property_id>\w+)/bookings',
    PropertyBookingsViewSet, 
    basename='properties_bookings',
    )

router.register(
    r'users/(?P<user_id>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/bookings',
    UserBookingsViewSet, 
    basename='users_bookings',
    )

urlpatterns = router.urls + [
    url('book/', BookingCreateView.as_view(), name="booking"),
    url('register/', Registration.as_view(), name="register"),    
]

