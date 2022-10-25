from time import sleep
from BillDash.models import Server, Bill, Customer
import datetime
from BillDash.models import pterodactyl
from django.utils import timezone
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs billing checks"

    def handle(self, *args, **kwargs):
        # generate the bills.
        for server in Server.objects.all():
            next_bill_date = server.next_payment_date - datetime.timedelta(days=7)
            if next_bill_date <= timezone.now():
                if Bill.objects.filter(server=server, paid=False).count() > 0:
                    continue
                bill = Bill(
                    server=server,
                    currency="INR",
                    amount=server.plan.price,
                    creation_date=datetime.datetime.now(),
                    due_date=datetime.datetime.now() + datetime.timedelta(days=7),
                    paid=False,
                )
                bill.save()
        # Suspend the servers.
        for server in Server.objects.all():
            if server.next_payment_date <= timezone.now() and not server.suspended:
                pterodactyl.suspend_server(server.server_id)
                server.suspended = True
                server.save()
