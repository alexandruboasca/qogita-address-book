from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import Country, State, Locality, Address


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'code', )

    def post(self, request, *args, **kwargs):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.created_by = self.request.user
            serializer.save()


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('name', 'code', 'country', )

    def post(self, request, *args, **kwargs):
        serializer = StateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.created_by = self.request.user
            serializer.save()


class LocalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Locality
        fields = ('name', 'postal_code', 'state', )

    def post(self, request, *args, **kwargs):
        serializer = LocalitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.created_by = self.request.user
            serializer.save()


class AddressSerializer(serializers.ModelSerializer):
    locality_name = serializers.SerializerMethodField()
    locality_postal_code = serializers.SerializerMethodField()
    state_name = serializers.SerializerMethodField()
    state_code = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()
    country_code = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField(
        required=False,
    )

    def get_locality_name(self, obj):
        if obj.locality:
            return obj.locality.name

    def get_locality_postal_code(self, obj):
        if obj.locality:
            return obj.locality.postal_code

    def get_state_name(self, obj):
        if obj.locality and obj.locality.state:
            return obj.locality.state.name

    def get_state_code(self, obj):
        if obj.locality and obj.locality.state:
            return obj.locality.state.code

    def get_country_name(self, obj):
        if obj.locality and obj.locality.state and obj.locality.state.country:
            return obj.locality.state.country.name

    def get_country_code(self, obj):
        if obj.locality and obj.locality.state and obj.locality.state.country:
            return obj.locality.state.country.code

    def get_created_by(self, obj):
        return obj.created_by.username

    class Meta:
        model = Address
        fields = ('street_number', 'route', 'locality_name',
                  'locality_postal_code', 'state_name', 'state_code',
                  'country_name', 'country_code', 'latitude', 'longitude',
                  'created_by', )
        # Assuming an address in distinct if all fields are different
        # In reality the unique check would probably include just a subset
        # of the address fields, such as street_number and locality
        validators = [
            UniqueTogetherValidator(
                queryset=Address.objects.all(),
                fields=['street_number', 'route', 'latitude', 'longitude', ]
            )
        ]
