import logging

logging.basicConfig(  # filename="uptime.log",
    format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
    level=logging.DEBUG)
import argparse
import ipaddress
import os
import sys
import pyICMP
import getmac
import netifaces
from typing import List


def get_IP_on_default_network() -> List[str]:
    gws = netifaces.gateways()
    default_interface = gws['default'][2][1]
    addr = netifaces.ifaddresses(default_interface)

    ip = addr[2][0]['addr']
    netmask = addr[2][0]['netmask']
    net = ipaddress.IPv4Network(ip + "/" + netmask, strict=False)

    device_list = []
    for i in net.hosts():
        device_list.append(str(i))

    return device_list


def get_mac_if_alive(ip: str):
    mac = False
    if pyICMP.ping(ip) is True:
        mac = getmac.get_mac_address(ip=ip)
    return mac


class device:
    def __init__(self):
        ip = ""
        mac_address = ""


class main:

    @staticmethod
    def run_main():
        """ Take arguments and direct program """
        parser = argparse.ArgumentParser()

        parser.add_argument("-ip", help="IP address in CIDR notation ex 192.168.1.0/24",
                            required=True)

        args = parser.parse_args()
        if len(sys.argv) == 1:  # Displays help and lists servers (to help first time users)
            parser.print_help()
            sys.exit(1)

        # Feeds generated IP host list tp sensor data generator
        device_list = []
        for i in ipaddress.IPv4Network(args.ip).hosts():
            device_list.append(device(str(i)))

        logging.info("EOP")


if __name__ == "__main__":
    logging.info("START")
    logging.info(str(os.getcwd()))

    print(get_mac_if_alive("192.168.11.1"))

    # main.run_main()
