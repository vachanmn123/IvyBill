import re
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from BillDash.models import Bill, Server
from .pterodactyl import Pterodactyl
import json

# Create your views here.\
@login_required
def index(request: HttpRequest):
    secrets = json.load(open("secrets.json"))
    ptero_url = secrets["pterodactyl_url"]
    contents = {"ptero_url": ptero_url}
    return render(request, "BillDash/index.html", contents)


@login_required
def bills(request: HttpRequest):
    return render(request, "BillDash/bills.html")


@login_required
def view_bill(request: HttpRequest, bill_no: int):
    if not Bill.objects.get(ok=bill_no):
        return redirect("/")
    bill = Bill.objects.get(pk=bill_no)
    context = {"bill": bill}
    return render(request, "BillDash/view_bill.html", context)


@login_required
def pay_bill(request: HttpRequest, bill_no: int):
    if not Bill.objects.get(pk=bill_no):
        return redirect("/")
    bill = Bill.objects.get(pk=bill_no)
    if bill.paid:
        return redirect("view_bill", bill_no=bill_no)
    context = {"bill": bill}
    return render(request, "BillDash/pay_bill.html", context)


@login_required
def server_info(request: HttpRequest, server_id: int):
    if not Server.objects.filter(server_id=server_id).exists():
        return redirect("index")
    ptero = Pterodactyl(
        json.load(open("secrets.json"))["pterodactyl_token"],
        json.load(open("secrets.json"))["pterodactyl_url"],
    )
    server = ptero.get_server_info(server_id)
    context = {
        "ptero_server": server,
        "db_server": Server.objects.get(server_id=server_id),
        "ptero_url": json.load(open("secrets.json"))["pterodactyl_url"],
    }
    return render(request, "BillDash/server_info.html", context)
