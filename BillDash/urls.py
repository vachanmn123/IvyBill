from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("bills", views.bills, name="bills"),
    path("viewbill/<int:bill_no>/", views.view_bill, name="view_bill"),
    path("paybill/<int:bill_no>/", views.pay_bill, name="pay_bill"),
    path("serverinfo/<int:server_id>/", views.server_info, name="server_info"),
]
