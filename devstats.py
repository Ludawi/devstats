import platform
import socket
import subprocess
import yaml


class Device:
    """Interface for device lookup, ping validation, and inventory import."""

    _CONFIG_FILE = "./config.yml"
    _PREAMBLE = [""]
    _POSTAMBLE = [""]
    _CONFIG_LOADED = False

    def __init__(self, service_tag):
        self.service_tag = service_tag
        self.hostname = None
        self.fqdn = None
        self.ip = None
        self.pingable = False
        self.hostname_replacement = None

    def __repr__(self):
        return (
            f"Device(service_tag='{self.service_tag}', hostname='{
                self.hostname}', "
            f"fqdn='{self.fqdn}', ip='{self.ip}', pingable={self.pingable}, "
            f"hostname_replacement='{self.hostname_replacement}')"
        )

    # --- Configuration Helpers ---

    @classmethod
    def _load_config(cls):
        """Loads the YAML configuration file."""
        if cls._CONFIG_LOADED:
            return

        try:
            with open(cls._CONFIG_FILE, "r") as config:
                data = yaml.safe_load(config) or {}
        except OSError:
            cls._CONFIG_LOADED = True
            return

        pre = data.get("hostname_preamble")
        post = data.get("hostname_postamble")

        if pre:
            cls._PREAMBLE = pre if isinstance(pre, list) else [pre]
        if post:
            cls._POSTAMBLE = post if isinstance(post, list) else [post]

        cls._CONFIG_LOADED = True

    @classmethod
    def _assemble_hostnames(cls, service_tag):
        """Generates all candidate hostnames based on config values."""
        cls._load_config()
        hostnames = []
        for pre in cls._PREAMBLE:
            for post in cls._POSTAMBLE:
                hostnames.append(f"{pre}{service_tag}{post}")
        return hostnames

    # --- Public Methods ---

    @classmethod
    def ip_lookup(cls, hostname):
        """Resolves a given hostname string to an IPv4 address."""
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None
        except Exception as e:
            print(f"[Info] Error looking up {hostname}: {e}")
            return None

    @classmethod
    def ping(cls, ip):
        """Pings an IP address and returns True if successful, False otherwise."""
        if not ip:
            return False
        param = "-n" if platform.system() == "Windows" else "-c"
        command = ["ping", param, "2", ip]

        try:
            result = subprocess.run(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except Exception as e:
            print(f"[Info] Failed to ping {ip}: {e}")
            return False

    # --- Public Interfaces ---

    @classmethod
    def get_ip(cls, service_tag):
        """Returns IPv4 address string of a device based on its service tag."""
        candidate_hostnames = cls._assemble_hostnames(service_tag)
        for candidate in candidate_hostnames:
            ip = cls.ip_lookup(candidate)
            if ip:
                return ip
        return None

    @classmethod
    def get_inventory(cls, service_tag):
        """Processes a service tag and returns an initialized Device instance

        containing fqdn, hostname, ip, ping status, and replacements.
        """
        device = cls(service_tag=service_tag)
        candidate_hostnames = cls._assemble_hostnames(service_tag)

        for candidate in candidate_hostnames:
            ip = cls.ip_lookup(candidate)
            if ip:
                device.ip = ip
                device.pingable = cls.ping(ip)

                try:
                    actual_fqdn, _, _ = socket.gethostbyaddr(ip)
                    device.fqdn = actual_fqdn

                    if actual_fqdn.lower() != candidate.lower():
                        device.hostname = candidate
                        device.hostname_replacement = actual_fqdn
                    else:
                        device.hostname = candidate
                except socket.herror:
                    device.hostname = candidate
                    device.fqdn = candidate

                return device

        return device


# --- EXAMPLES ---
# if __name__ == "__main__":
#
#     # 1. Quick IP lookup directly from the class
#     ip_address = Device.get_ip("google")
#     print(f"IP: {ip_address}")
#
#     print("---")
#
#     # 2. Complete Inventory validation returning the populated class object
#     my_device = Device.get_inventory("1984-0")
#     print("Populated Device Object Attributes:")
#     print(f" -> Service Tag: {my_device.service_tag}")
#     print(f" -> Hostname:    {my_device.hostname}")
#     print(f" -> FQDN:        {my_device.fqdn}")
#     print(f" -> IP:          {my_device.ip}")
#     print(f" -> Ping:        {my_device.pingable}")
