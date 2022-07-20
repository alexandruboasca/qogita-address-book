from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_created_by'
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        blank=True,
    )

    class Meta:
        abstract = True


class Country(BaseModel):
    name = models.CharField(max_length=40, unique=True, blank=True)
    code = models.CharField(max_length=2, blank=True)


class State(BaseModel):
    name = models.CharField(max_length=165, blank=True)
    code = models.CharField(max_length=8, blank=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="states"
    )


class Locality(BaseModel):
    name = models.CharField(max_length=165, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="localities"
    )

    class Meta:
        verbose_name_plural = "Localities"
        unique_together = ("name", "postal_code", "state")
        ordering = ("state", "name")


class Address(BaseModel):
    street_number = models.CharField(max_length=20, blank=True)
    route = models.CharField(max_length=100, blank=True)
    locality = models.ForeignKey(
        Locality,
        on_delete=models.CASCADE,
        related_name="addresses",
        blank=True,
        null=True,
    )
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ("locality", "route", "street_number")