from scapy.all import *
import sys, argparse, multiprocessing, logging
from datetime import datetime
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
conf.verb = 0

def scanPort(ip, port):
    srcp = RandShort()
    pkt = sr1(IP(dst=ip) / TCP(sport=srcp, dport=port, flags="S"))
    flag = pkt.getlayer(TCP).flags
    if flag == 0x12:
        print("[+] Port " + str(port) + " open")
        send(IP(dst=ip) / TCP(sport=srcp, dport=port, flags="R"))

def main(args):
    start = datetime.now()
    args.throttle = float(args.throttle)
    print ("============================================================")
    print ("Stealh Port Scanning " + args.IP + " for ports " + str(args.sport)
        + " - " + str(args.eport))
    print ("Started @ " + str(start))
    print ("============================================================")
    for port in range(int(args.sport), int(args.eport+1)):
        p = multiprocessing.Process(target=scanPort, args=(args.IP, port))
        p.start()
        time.sleep(args.throttle)
    time.sleep(3)
    stop = datetime.now()
    print ("============================================================")
    print ("Scan Duration: " + str(stop - start))
    print ("Completed @ " + str(stop))
    print ("============================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", action="store", help="IP to port scan", type=str)
    parser.add_argument("sport", action="store", nargs='?', default=1,
        const=1, help="Start Port Range", type=int)
    parser.add_argument("eport", action="store", nargs='?', default=1023,
        const=1023, help="End Port Range", type=int)
    parser.add_argument("-t", "--throttle", action="store",
        help="throttle connection attempts", nargs='?', default=0.25, const=0.25)

    if len(sys.argv[1:]) == 0:
        parser.parse_args()
        parser.exit()

    args = parser.parse_args()
    main(args)