from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication,\
    BasicAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Country, State, Locality, Address
from .serializers import AddressSerializer
from django_filters.rest_framework import DjangoFilterBackend


class AddressList(generics.ListCreateAPIView):
    FILTER_SEARCH_FIELDS = (
        'street_number',
        'latitude',
        'longitude',
        'locality__name',
        'locality__postal_code',
        'locality__state__name',
        'locality__state__code',
        'locality__state__country__name',
        'locality__state__country__code',
    )
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = FILTER_SEARCH_FIELDS
    search_fields = FILTER_SEARCH_FIELDS
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        user = self.request.user
        # Only return the addresses of the user
        return super().get_queryset().filter(created_by=user)

    def post(self, request, *args, **kwargs):
        data = request.data
        country, created = Country.objects.get_or_create(
            name=data['country_name'],
            code=data['country_code'],
            created_by=self.request.user,
        )
        state, _ = State.objects.get_or_create(
            name=data['state_name'],
            code=data['state_code'],
            country=country,
            created_by=self.request.user,
        )
        locality, _ = Locality.objects.get_or_create(
            name=data['locality_name'],
            postal_code=data['locality_postal_code'],
            state=state,
            created_by=self.request.user,
        )

        new_data = {
            'created_by': self.request.user,
            'street_number': data['street_number'],
            'locality': locality,
            'route': data['route'],
            'latitude': data['latitude'],
            'longitude': data['longitude'],
        }

        serializer = AddressSerializer(data=new_data)
        if serializer.is_valid(raise_exception=True):
            address = Address(**new_data)
            address.save()
            return Response({}, status=status.HTTP_201_CREATED)


class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
