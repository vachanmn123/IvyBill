from importlib.resources import contents
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from .pterodactyl import Pterodactyl
import json

# Create your views here.\
@login_required
def index(request: HttpRequest):
    secrets = json.load(open("secrets.json"))
    contents = {"user": request.user}
    return render(request, "BillDash/index.html")
