from ast import Str
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

# from BillDash.models import Bill, Server

webhook_url = json.load(open("secrets.json", "r"))["discord_webhook"]


def new_bill(bill):
    embed = DiscordEmbed(
        title=f"New bill for {str(bill.server.customer)}",
        description=f"Amount: {bill.amount} {bill.currency}",
        color=0x00FF00,
    )
    embed.add_embed_field(name="Bill Number", value=str(bill.bill_number))
    embed.add_embed_field(name="Server", value=str(bill.server))
    embed.add_embed_field(
        name="Due date", value=f"<t:{int(bill.due_date.timestamp())}>"
    )
    embed.add_embed_field(name="Amount", value=f"{bill.amount} {bill.currency}")
    webhook = DiscordWebhook(url=webhook_url, embeds=[embed])
    webhook.execute()


def new_server(server):
    embed = DiscordEmbed(
        title=f"New server for {str(server.customer)}",
        description=f"Server: {str(server)}",
        color=0x00FF00,
    )
    embed.add_embed_field(name="Server Name", value=str(server))
    embed.add_embed_field(name="Server ID", value=server.server_id_hex)
    embed.add_embed_field(name="Server Software", value=str(server.server_software))
    embed.add_embed_field(name="Server Plan", value=str(server.plan))
    embed.add_embed_field(name="Server Owner", value=str(server.customer))
    webhook = DiscordWebhook(url=webhook_url, embeds=[embed])
    webhook.execute()


def suspend_server(server):
    embed = DiscordEmbed(
        title=f"Suspended server for {str(server.customer)}",
        description=f"Server: {str(server)}",
        color=0xFF0000,
    )
    embed.add_embed_field(name="Server Name", value=str(server))
    embed.add_embed_field(name="Server ID", value=server.server_id_hex)
    embed.add_embed_field(name="Server Software", value=str(server.server_software))
    embed.add_embed_field(name="Server Plan", value=str(server.plan))
    embed.add_embed_field(name="Server Owner", value=str(server.customer))
    embed.add_embed_field(
        name="Server Creation Date",
        value=f"<t:{int(server.creation_date.strftime('%s'))}>",
    )
    webhook = DiscordWebhook(url=webhook_url, embeds=[embed])
    webhook.execute()


def unsuspend_server(server):
    embed = DiscordEmbed(
        title=f"Unsuspended server for {str(server.customer)}",
        description=f"Server: {str(server)}",
        color=0xFF0000,
    )
    embed.add_embed_field(name="Server Name", value=str(server))
    embed.add_embed_field(name="Server ID", value=server.server_id_hex)
    embed.add_embed_field(name="Server Software", value=str(server.server_software))
    embed.add_embed_field(name="Server Plan", value=str(server.plan))
    embed.add_embed_field(name="Server Owner", value=str(server.customer))
    embed.add_embed_field(
        name="Server Creation Date",
        value=f"<t:{int(server.creation_date.strftime('%s'))}>",
    )
    webhook = DiscordWebhook(url=webhook_url, embeds=[embed])
    webhook.execute()


def delete_server(server):
    embed = DiscordEmbed(
        title=f"Deleted server for {str(server.customer)}",
        description=f"Server: {str(server)}",
        color=0xFF0000,
    )
    embed.add_embed_field(name="Server Name", value=str(server))
    embed.add_embed_field(name="Server ID", value=server.server_id_hex)
    embed.add_embed_field(name="Server Software", value=str(server.server_software))
    embed.add_embed_field(name="Server Plan", value=str(server.plan))
    embed.add_embed_field(name="Server Owner", value=str(server.customer))
    embed.add_embed_field(
        name="Server Creation Date",
        value=f"<t:{int(server.creation_date.strftime('%s'))}>",
    )
    webhook = DiscordWebhook(url=webhook_url, embeds=[embed])
    webhook.execute()


def bill_paid(bill):
    try:
        embed = DiscordEmbed(
            title=f"Bill marked paid for {str(bill.server.customer)}",
            description=f"Amount: {bill.amount} {bill.currency}",
            color=0x00FF00,
        )
    except:
        embed = DiscordEmbed(
            title=f"Bill marked paid for {str(bill.server)}",
            description=f"Amount: {bill.amount} {bill.currency}",
            color=0x00FF00,
        )
    embed.add_embed_field(name="Bill Number", value=str(bill.bill_number))
    embed.add_embed_field(name="Server", value=str(bill.server))
    embed.add_embed_field(
        name="Due date", value=f"<t:{int(bill.due_date.timestamp())}>"
    )
    embed.add_embed_field(name="Amount", value=f"{bill.amount} {bill.currency}")
    webhook = DiscordWebhook(url=webhook_url, embeds=[embed])
    webhook.execute()


def bill_delete(bill):
    try:
        embed = DiscordEmbed(
            title=f"Bill deleted for {str(bill.server.customer)}",
            description=f"Amount: {bill.amount} {bill.currency}",
            color=0xFF0000,
        )
    except:
        embed = DiscordEmbed(
            title=f"Bill deleted for {str(bill.server)}",
            description=f"Amount: {bill.amount} {bill.currency}",
            color=0x00FF00,
        )
    embed.add_embed_field(name="Bill Number", value=str(bill.bill_number))
    embed.add_embed_field(name="Server", value=str(bill.server))
    embed.add_embed_field(
        name="Due date", value=f"<t:{int(bill.due_date.timestamp())}>"
    )
    embed.add_embed_field(name="Amount", value=f"{bill.amount} {bill.currency}")
    embed.add_embed_field(name="Paid", value=str(bill.paid))
    webhook = DiscordWebhook(url=webhook_url, embeds=[embed])
    webhook.execute()
