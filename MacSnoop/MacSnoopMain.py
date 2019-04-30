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


class Device:
    ip = ""
    mac_address = ""

    def __init__(self, ip, mac_address):
        self.ip = ip
        self.mac_address = mac_address


class main:

    @staticmethod
    def run_main():
        """ Take arguments and direct program """
        # parser = argparse.ArgumentParser()
        #
        # parser.add_argument("-ip", help="IP address in CIDR notation ex 192.168.1.0/24",
        #                     required=True)
        #
        # args = parser.parse_args()
        # if len(sys.argv) == 1:  # Displays help and lists servers (to help first time users)
        #     parser.print_help()
        #     sys.exit(1)
        #
        raw_ip_list = []

        for raw_ip in get_IP_on_default_network():
            raw_ip_list.append(str(raw_ip))

        live_list = []
        for ip in raw_ip_list:
            mac = get_mac_if_alive(ip)
            if mac:
                live_list.append(Device(ip, mac))

        logging.info("EOP")


if __name__ == "__main__":
    logging.info("START")
    logging.info(str(os.getcwd()))
    main.run_main()
