from scapy.interfaces import NetworkInterface, get_working_ifaces
from typing import Dict, Never
import sys

from scapy.layers.l2 import srp1

TEST_MAC_ADDR = "4b:54:55:53:45:43"  # The MAC Address for tests


def filter_task_frames(frame):
    """
    Filter only ARP packets that has 4b:54:55:53:45:43 mac address
    for make testing easiest
    """
    return frame.src == TEST_MAC_ADDR or frame.dst == TEST_MAC_ADDR


def get_response(frame, iface):
    response = srp1(frame, timeout=1, iface=iface)
    if response is not None:
        if filter_task_frames(response):
            return response
    return None


def get_iface() -> NetworkInterface | Never:
    ifaces = get_working_ifaces()
    if len(sys.argv) > 1:
        iface_name = sys.argv[-1]
        for iface in ifaces:
            if iface_name == iface.name:
                return iface
        else:
            raise RuntimeError(f"{iface_name} is not found!")
    else:
        for iface in ifaces:
            if iface.ip == "127.0.0.1" or iface.name.startswith("lo"):
                return iface
        else:
            raise RuntimeError("No Interface configured")
