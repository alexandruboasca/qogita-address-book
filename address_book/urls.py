from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from address_book import views

urlpatterns = [
    path(
        'address',
        views.AddressList.as_view(),
        name='address-list'
    ),
    path(
        'address/<int:pk>',
        views.AddressDetail.as_view(),
        name='address-detail'
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
