from devstats import Device

# 1. Quick IP lookup directly from the class
ip_address = Device.get_ip("google")
print(f"IP: {ip_address}")

print("---")

# 2. Complete Inventory validation returning the populated class object
my_device = Device.get_inventory("googe")
print("Device Object Attributes:")
print(f" -> Service Tag: {my_device.service_tag}")
print(f" -> Hostname:    {my_device.hostname}")
print(f" -> FQDN:        {my_device.fqdn}")
print(f" -> IP:          {my_device.ip}")
print(f" -> Ping:        {my_device.pingable}")
