#!/usr/bin/env python3
import argparse
from devstats import Device


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool to look up devices status by service tag or hostname."
    )

    # Define the expected parameter
    parser.add_parser_parameters = parser.add_argument(
        "target",
        type=str,
        help="The service tag or hostname of the device to inspect.",
    )
    args = parser.parse_args()

    print(f"Fetching: {args.target}...")
    print("-----")

    # Perform the inventory validation using the parameter
    device = Device.get_inventory(args.target)

    # Output the results
    if device.ip:
        print("Device Object Attributes:")
        print(f" -> Service Tag: {device.service_tag}")
        print(f" -> Hostname:    {device.hostname}")
        print(f" -> FQDN:        {device.fqdn}")
        print(f" -> IP:          {device.ip}")
        print(f" -> Ping:        {device.pingable}")
    else:
        print(
            f"[Error] Could not find or resolve any records for '{
                args.target}'."
        )


if __name__ == "__main__":
    main()
