import multiprocessing, sys, netaddr, argparse, logging
from scapy.all import *
from datetime import datetime
logging.getLogger("scapy.runetime").setLevel(logging.ERROR)
conf.verb = 0

class const:
    ARP = 0
    PING = 1
    TCP = 2

def arpScan(subnet):
    ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet), timeout=2)
    for snd,rcv in ans:
        print(rcv.sprintf(r"[ARP] Online: %ARP.psrc% - %Ether.src%"))

def ping(ip):
    reply = sr1(IP(dst=str(ip)) / ICMP(), timeout = 3)
    if reply is not None:
        print("[PING] Online: " + str(ip))

def tcp(ip):
    port = 53
    srcp = RandShort()
    pkt = sr1(IP(dst = str(ip)) / TCP(sport = srcp, dport = port, flags = "S"), timeout = 5)
    if pkt is not None:
        flag = pkt.getlayer(TCP).flags
        if flag == 0x12: #syn,ack
            print("[TCP] Online:" + str(ip) + " - replied with syn,ack")
            send(IP(dst = str(ip)) / TCP(sport = srcp, dport = port, flags = "R"))
        elif flag == 0x14: # RST
            print("[TCP] Online: " + str(ip) + " - replied with rst,ack")

def scan(subnet, typ):
    jobs = []
    for ip in subnet:
        if typ == const.PING:
            p = multiprocessing.Process(target=ping, args=(ip,))
            jobs.append(p)
            p.start()
        else:
            p = multiprocessing.Process(target=tcp, args=(ip,))
            jobs.append(p)
            p.start()

    for j in jobs:
        j.join()

def main(args):
    subnet = netaddr.IPNetwork(args.subnet)
    start = datetime.now()
    print ("==================================================")
    print ("Scanning " + str(subnet[0]) + " to " + str(subnet[-1]))
    print ("Started @ " + str(start))
    print ("==================================================")

    if args.scantype == const.ARP:
        arpScan(args.subnet)
    elif args.scantype == const.PING:
        scan(subnet, const.PING)
    elif args.scantype == const.TCP:
        scan(subnet, const.TCP)
    else:
        arpScan(args.subnet)
        scan(subnet, const.PING)
        scan(subnet, const.TCP)

    stop = datetime.now()
    print ("==================================================")
    print ("Scan Duration: " + str(stop - start))
    print ("Completed @ " + str(stop))
    print ("==================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subnet", action="store", help="Subnet to scan for hosts", type=str)
    parser.add_argument("scantype", action="store", nargs="?", default=3,
        help="Type of scan: [0 = Arp, 1 = Ping, 2 = TCP, 3 = ALL]", type=int)

    if len(sys.argv[1:])==0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    main(args)