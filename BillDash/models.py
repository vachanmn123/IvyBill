from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.PROTECT, default=None
    )
    name = models.CharField(max_length=25)
    ptero_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    def email(self):
        return self.user.email


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    paid = models.BooleanField(default=False)


class Plan(models.Model):
    ram = models.IntegerField(default=0)
    cpu = models.IntegerField(default=0)
    disk = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=25)
    network_allocations = models.IntegerField(default=1)
    backups = models.IntegerField(default=0)
    databases = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Server(models.Model):
    server_id = models.IntegerField()
    server_id_hex = models.CharField(max_length=10)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    creation_date = models.TimeField(auto_now=True)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    ram = models.IntegerField(default=0)
    cpu = models.IntegerField(default=0)
    disk = models.IntegerField(default=0)
    next_payment_date = models.DateTimeField(null=True, blank=True)
    last_payment = models.OneToOneField(
        Payment, null=True, blank=True, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.server_id_hex
