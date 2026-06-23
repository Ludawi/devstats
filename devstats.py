import subprocess
import yaml
import socket
import platform

CONFIG_FILE = "./config.yml"
DNS_SERVER = "1.1.1.1"


def create_runtime_conf():
    global conf
    global preamble
    global postamble

    try:
        with open(CONFIG_FILE, "r") as config:
            data = yaml.safe_load(config)
    except OSError:
        print(f"No config file found at {CONFIG_FILE}")
        return -1

    preamble = data["hostname_preamble"]
    postamble = data["hostname_postamble"]

    if type(preamble) is list or preamble is None:
        if len(preamble) == 0:
            preamble = [""]
        else:
            pass

    if type(postamble) is list or preamble is None:
        if len(postamble) == 0:
            postamble = [""]
        else:
            pass

    conf = True
    return


class Device:
    """Provides all neccessary data for importing a new device (service tag)
        returns:
            - fqdn  string
            - ip    string
            - ping  bool
    """

    def __init__(self):
        self.service_tag
        self.fqdn
        self.ip


def assemble_hostnames(service_tag):
    hostnames = []

    for i in preamble:
        if preamble is None:
            pass
        else:
            hostname_pre = f"{i}{service_tag}"
        for n in postamble:
            if postamble is None:
                pass
            else:
                hostname = f"{hostname_pre}{n}"
                hostnames.append(hostname)
                hostname = ""

    return hostnames


def ip_lookup(hostname):
    try:
        # Resolve the hostname to an IPv4 address
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        # gaierror happens if the hostname cannot be resolved (NXDOMAIN)
        print(f"[Info] Could not resolve hostname: {hostname}")
        return None
    except Exception as e:
        # Catches other potential issues like network timeouts
        print(f"[Info] Error looking up {hostname}: {e}")
        return None
    pass


def ping(ip):
    #  Assemble parameters based on platform
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


create_runtime_conf()


def inventory_import(service_tag):
    """Provides all neccessary data for importing a new device (service tag)
        returns:
            - fqdn  string
            - ip    string
            - ping  bool
    """
    hostnames = assemble_hostnames("google")
    for i in hostnames:
        current_ip = ip_lookup(i)
        if current_ip is not None:
            res = ping(current_ip)
            print(res)
