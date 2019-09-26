from rest_framework import serializers
from .models import User, Booking, Property


class PropertySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='property_id', required=False)
    class Meta:
        model = Property
        exclude = ()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='uuid')
    name = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ('id', 'name',)


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    property = PropertySerializer()

    class Meta:
        model = Booking
        fields = ('user', 'property')
    
    def create(self, validated_data):
        validated_data.pop('user', None)
        property = validated_data.pop('property')
        p, _ = Property.objects.get_or_create(**property)

        booking = Booking.objects.create(
            property=p, user=self.context['request'].user, **validated_data)

        return booking


class PropertyBookingsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    id = serializers.CharField(source='uuid')
    property_name = serializers.CharField(source='property.property_name', read_only=True)
    property_id = serializers.CharField(source='property.property_id', read_only=True)
    city = serializers.CharField(source='property.city', read_only=True)

    class Meta:
        model = Booking
        fields = ('user', 'id', 'property_name', 'property_id', 'city',)


class UserBookingsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='uuid')
    property_name = serializers.CharField(source='property.property_name', read_only=True)
    property_id = serializers.CharField(source='property.property_id', read_only=True)
    city = serializers.CharField(source='property.city', read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'property_name', 'property_id', 'city',)
