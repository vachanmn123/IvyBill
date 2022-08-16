from dataclasses import fields
from django.contrib import admin

from .models import Customer, Server, Plan, Bill, Location, ServerSoftware

# Register your models here.
admin.site.register(Bill)
admin.site.site_header = "IvyBill Admin"


class ServerInLine(admin.TabularInline):
    model = Server
    extra = 0
    fields = ("server_id_hex", "next_payment_date", "plan")
    readonly_fields = ("server_id_hex", "next_payment_date", "plan")
    can_delete = False
    verbose_name = "Server"
    verbose_name_plural = "Servers"


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("ptero_id", "name", "email")
    search_fields = ["ptero_id", "email"]
    inlines = [ServerInLine]
    readonly_fields = ["ptero_id"]


class ServerAdmin(admin.ModelAdmin):
    list_display = ("server_id_hex", "next_payment_date", "plan", "customer")
    search_fields = ["server_id_hex"]
    readonly_fields = ["server_id_hex", "server_id", "creation_date"]
    ordering = ["server_id"]
    fieldsets = [
        (
            "Customer and Payment",
            {"fields": ["customer", "next_payment_date", "creation_date"]},
        ),
        ("Server Info", {"fields": ["plan", "server_software"]}),
        ("Pterodactyl Info", {"fields": ["server_id_hex", "server_id"]}),
    ]
    can_delete = False
    verbose_name = "Server"
    verbose_name_plural = "Servers"


class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "ptero_id")
    search_fields = ["name"]
    ordering = ["ptero_id"]


class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "ram", "cpu", "disk", "location", "price")
    search_fields = ["name"]
    fieldsets = [
        ("Plan Info", {"fields": ["name", "price"]}),
        ("Resource Limits", {"fields": ["ram", "cpu", "disk"]}),
        ("Location", {"fields": ["location"]}),
        (
            "features",
            {"fields": ["network_allocations", "backups", "databases", "dedicated_ip"]},
        ),
    ]
    ordering = ["price"]


class ServerSoftwareAdmin(admin.ModelAdmin):
    list_display = ("name", "game_name", "ptero_egg_id")
    search_fields = ["name", "game_name"]
    ordering = ["ptero_egg_id"]
    inlines = [ServerInLine]
    readonly_fields = ["docker_image", "startup_command", "environment"]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(ServerSoftware, ServerSoftwareAdmin)
