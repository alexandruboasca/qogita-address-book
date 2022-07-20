from django.contrib import admin
from .models import Country, State, Locality, Address


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
