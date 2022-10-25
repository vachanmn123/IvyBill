from typing_extensions import Required
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from .pterodactyl import Pterodactyl
import json
from . import notify
from django.utils import timezone

from BillDash import pterodactyl

pterodactyl = Pterodactyl(
    json.load(open("secrets.json"))["pterodactyl_token"],
    json.load(open("secrets.json"))["pterodactyl_url"],
)

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.PROTECT, default=None
    )
    name = models.CharField(max_length=25)
    ptero_id = models.IntegerField(blank=True, null=True, default=None)

    def __str__(self) -> str:
        return self.name

    def email(self):
        return self.user.email

    def save(self, *args) -> None:
        if self.ptero_id is not None:
            return super().save(*args)
        res = pterodactyl.create_new_user(
            self.user.email,
            self.user.username,
            self.user.first_name,
            self.user.last_name,
        )
        if res is None:
            return print("Error creating customer")
        self.ptero_id = int(res["attributes"]["id"])
        return super().save(*args)

    def delete(self, *args):
        print("Deleting customer")
        if pterodactyl.delete_user(self.ptero_id):
            return super().delete(*args)
        return print("Error deleting customer")


class Bill(models.Model):
    bill_number = models.AutoField(primary_key=True)
    server = models.ForeignKey("Server", on_delete=models.SET_NULL, null=True)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        try:
            return f"{self.server.customer} - {self.due_date.isoformat()}"
        except:
            return f"{self.server} - {self.due_date.isoformat()}"

    def save(self, *args) -> None:
        if (not self._state.adding) and self.paid:
            self.server.next_payment_date += timezone.timedelta(days=30)
            return super().save(*args)
        if self.amount > 0:
            notify.new_bill(self)
            return super().save(*args)
        self.amount = self.server.plan.price
        notify.new_bill(self)
        return super().save(*args)


class Location(models.Model):
    name = models.CharField(max_length=25)
    ptero_id = models.IntegerField(blank=True, null=True, default=None)

    def __str__(self) -> str:
        return self.name


class Plan(models.Model):
    ram = models.IntegerField(default=0)
    cpu = models.IntegerField(default=0)
    disk = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=25)
    network_allocations = models.IntegerField(default=1)
    backups = models.IntegerField(default=0)
    databases = models.IntegerField(default=0)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, default=None)
    dedicated_ip = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ServerSoftware(models.Model):
    name = models.CharField(max_length=25)
    game_name = models.CharField(max_length=25)
    ptero_nest_id = models.IntegerField(blank=False, null=False)
    ptero_egg_id = models.IntegerField(blank=False, null=False)
    docker_image = models.CharField(max_length=25, blank=True, null=True)
    startup_command = models.CharField(max_length=1000, blank=True, null=True)
    environment = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.game_name} - {self.name}"

    def save(self, *args) -> None:
        resp = pterodactyl.get_egg_info(self.ptero_nest_id, self.ptero_egg_id)
        if not resp:
            return "Error getting egg info"
        self.docker_image = resp["attributes"]["docker_image"]
        env = {}
        for var in resp["attributes"]["relationships"]["variables"]["data"]:
            env[f"{var['attributes']['env_variable']}"] = var["attributes"][
                "default_value"
            ]
        self.environment = json.dumps(env)
        self.startup_command = resp["attributes"]["startup"]
        return super().save(*args)


class Server(models.Model):
    server_id = models.IntegerField()
    server_id_hex = models.CharField(max_length=10, blank=True, null=True, default=None)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    creation_date = models.TimeField(auto_now=True)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    next_payment_date = models.DateTimeField(null=True, blank=True)
    server_software = models.ForeignKey(
        ServerSoftware, on_delete=models.PROTECT, default=None
    )
    suspended = models.BooleanField(default=False)

    def __str__(self):
        return self.server_id_hex

    def name(self):
        res = pterodactyl.get_server_info(self.server_id)
        if not res:
            return "Error getting server info"
        return res["attributes"]["name"]

    def save(self, *args):
        if not self._state.adding:
            if not self.suspended:
                notify.unsuspend_server(self)
                pterodactyl.unsuspend_server(self.server_id)
            if self.suspended:
                notify.suspend_server(self)
                pterodactyl.suspend_server(self.server_id)
            return super().save(*args)
        if self.server_id is not None:
            self.server_id_hex = pterodactyl.get_server_info(self.server_id)[
                "attributes"
            ]["identifier"]
            return super().save(*args)
        specs = {
            "name": f"{self.customer.name}-{self.plan.name}",
            "user": self.customer.ptero_id,
            "egg": self.server_software.ptero_egg_id,
            "docker_image": self.server_software.docker_image,
            "startup": self.server_software.startup_command,
            "environment": json.loads(self.server_software.environment),
            "limits": {
                "memory": self.plan.ram,
                "swap": -1,
                "disk": self.plan.disk,
                "io": 500,
                "cpu": self.plan.cpu,
            },
            "feature_limits": {
                "databases": self.plan.databases,
                "backups": self.plan.backups,
                "allocations": self.plan.network_allocations,
            },
            "deploy": {
                "location": [self.plan.location.ptero_id],
                "dedicated_ip": self.plan.dedicated_ip,
            },
        }
        res = pterodactyl.create_new_server(
            specs["name"],
            specs["user"],
            specs["egg"],
            specs["docker_image"],
            specs["startup"],
            specs["environment"],
            specs["limits"],
            specs["feature_limits"],
            specs["deploy"]["location"],
            specs["deploy"]["dedicated_ip"],
        )
        if res == None:
            return print("Error creating server")
        self.server_id = res["attributes"]["id"]
        self.server_id_hex = res["attributes"]["identifier"]
        notify.new_server(self)
        return super().save(*args)

    def delete(self, *args):
        pterodactyl.delete_server(self.server_id)
        notify.delete_server(self)
        return super().delete(*args)
