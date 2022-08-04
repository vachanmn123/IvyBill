from django.contrib import admin

from .models import Customer, Server, Plan, Payment

# Register your models here.
admin.site.register(Payment)
admin.site.site_header = "IvyBill Admin"


class ServerInLine(admin.TabularInline):
    model = Server
    extra = 0
    fields = ("server_id_hex", "ram", "cpu", "disk", "next_payment_date")
    readonly_fields = ("server_id_hex", "ram", "cpu", "disk", "next_payment_date")
    can_delete = False
    verbose_name = "Server"
    verbose_name_plural = "Servers"


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("ptero_id", "name", "email")
    search_fields = ["ptero_id", "email"]
    inlines = [ServerInLine]


class ServerAdmin(admin.ModelAdmin):
    list_display = ("server_id_hex", "ram", "cpu", "disk", "next_payment_date")
    search_fields = ["server_id_hex"]
    readonly_fields = ("server_id_hex", "ram", "cpu", "disk", "next_payment_date")
    can_delete = False
    verbose_name = "Server"
    verbose_name_plural = "Servers"


class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "ram", "cpu", "disk", "price")
    search_fields = ["name"]
    ordering = ["name", "ram", "cpu", "disk", "price"]
    inlines = [ServerInLine]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Plan, PlanAdmin)
