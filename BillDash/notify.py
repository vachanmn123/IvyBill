def new_bill(bill):
    print(f"New bill for {bill.server.customer}")


def new_server(server):
    print(f"New server for {server.customer}")


def suspend_server(server):
    print(f"Suspended server for {server.customer}")


def unsuspend_server(server):
    print(f"Unsuspended server for {server.customer}")


def delete_server(server):
    print(f"Deleted server for {server.customer}")
