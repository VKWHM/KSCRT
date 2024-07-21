from unittest import TestCase
import unittest

from scapy.fields import RandIP, RandMAC
from scapy.layers.l2 import ARP, Ether
from utils import get_iface, get_response
from utils import TEST_MAC_ADDR

INTERFACE = get_iface()  # Used Interface
IP_ADDR = INTERFACE.ip  # Self IP Address


class TestArpWhoHasRequest(TestCase):
    def setUp(self) -> None:
        self.req_ip = str(RandIP())
        self.req_mac = str(RandMAC())
        self.frame = Ether(
            src=TEST_MAC_ADDR, dst="ff:ff:ff:ff:ff:ff"  # Broadcasting
        ) / ARP(op=1, psrc=self.req_ip, hwsrc=self.req_mac, hwdst="00:00:00:00:00:00")
        return super().setUp()

    def test_get_response_of_arp_request(self):
        self.frame.pdst = INTERFACE.ip

        response = get_response(self.frame, INTERFACE)

        self.assertIsNotNone(response)

    def test_psrc_value_of_arp_response(self):
        self.frame.pdst = INTERFACE.ip

        response = get_response(self.frame, INTERFACE)

        if response is not None:
            self.assertEqual(response.payload.psrc, INTERFACE.ip)

    def test_hwsrc_value_of_arp_response(self):
        self.frame.pdst = INTERFACE.ip

        response = get_response(self.frame, INTERFACE)

        if response is not None:
            self.assertEqual(response.payload.hwsrc, INTERFACE.mac)

    def test_arp_request_to_different_host(self):
        self.frame.pdst = str(RandIP())

        response = get_response(self.frame, INTERFACE)

        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
