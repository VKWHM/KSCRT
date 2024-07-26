from scapy.layers.l2 import ARP, Ether
from utils import get_iface, filter_task_frames, TEST_MAC_ADDR
from scapy.all import sendp, sniff
from scapy.config import conf


INTERFACE = get_iface()  # Used Interface
IP_ADDR = INTERFACE.ip  # Self IP Address


detected_hosts: dict[str, str] = {}


def handle_packet(pkt):
    """
    Handle ARP messages and make response if neccessery
    """
    arp_pkt = pkt.payload
    match arp_pkt.op:
        case 1 if arp_pkt.pdst == IP_ADDR:  # Who-has ARP REQUEST
            response_packet = ARP(
                op=2,
                psrc=IP_ADDR,
                pdst=arp_pkt.psrc,
                hwsrc=INTERFACE.mac,
                hwdst=arp_pkt.hwsrc,
            )
            response_frame = (
                Ether(src=INTERFACE.mac, dst=TEST_MAC_ADDR) / response_packet
            )
            sendp(response_frame, iface=INTERFACE, verbose=False)

        case 2 if arp_pkt.pdst == IP_ADDR:  # Is-at ARP RESPONSE
            pkt_ip = arp_pkt.psrc
            pkt_mac = arp_pkt.hwsrc
            if pkt_ip in detected_hosts.keys():
                mac = detected_hosts[pkt_ip]
                if pkt_mac != mac:
                    print(f"[+] Host {pkt_ip} Updated!\t{mac} => {pkt_mac}")
                    detected_hosts[pkt_ip] = pkt_mac
            else:
                detected_hosts[pkt_ip] = pkt_mac
                print(f"[+] New IP: {pkt_ip}\tMAC: {pkt_mac}")

        case 1 | 2:
            for suffix in ["src", "dst"]:
                pkt_ip, pkt_mac = getattr(arp_pkt, f"p{suffix}"), getattr(
                    arp_pkt, f"hw{suffix}"
                )
                if not pkt_ip in detected_hosts.keys():
                    detected_hosts[pkt_ip] = pkt_mac
                    print(f"[*] Monitor detect IP: {pkt_ip}\tMAC: {pkt_mac}")
                elif detected_hosts[pkt_ip] != pkt_mac:
                    print(f"[*] Monitor detect new MAC to: {pkt_ip}\tMAC: {pkt_mac}")

        case _:  # Other ARP Types
            print(f"Unsupported ARP type from {arp_pkt.psrc}")


def main():
    sniff(
        count=0,  # infinity
        store=False,
        iface=INTERFACE,
        filter="arp",  # Only ARP packets
        lfilter=filter_task_frames,
        prn=handle_packet,
    )


if __name__ == "__main__":
    main()

