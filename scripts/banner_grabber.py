import sys, argparse, socket, multiprocessing, subprocess, time
from datetime import datetime

def scan(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        res = s.connect_ex((ip, port))
        if res == 0:
            if port == 80:
                rsp = "HEAD / HTTP/1.1\r\nhost: "+ ip + "\r\n\r\n"
                s.send(rsp.encode())
            banner = s.recv(4096)
            msg = "[+] Port " + str(port) + " open\n"
            msg += "------------------------\n" + banner.strip().decode()
            print(msg + "\n------------------------\n")
        s.close()
    except socket.timeout:
        banner = "No Banner Message"
        if port == 53:
            banner = subprocess.getoutput("nslookup -type=any -class=chaos version.bind " + ip)
        msg = "[+] Port " + str(port) + " open\n"
        msg += "------------------------\n" + banner.strip().decode()
        print(msg + "\n------------------------\n")
        s.close()

def main(args):
    try:
        args.throttle = float(args.throttle)
        start = datetime.now()
        print ("==================================================")
        print ("Scanning " + args.IP + " Ports: " + str(args.sport) + " - " + str(args.eport))
        print ("==================================================\n")
        ports = range(args.sport, args.eport+1)
        for port in ports:
            p = multiprocessing.Process(target=scan, args=(args.IP,port,))
            p.start()
            time.sleep(args.throttle)
        time.sleep(3)
        stop = datetime.now()
        print ("==================================================")
        print ("Scan Duration: " + str(stop - start))
        print ("==================================================")
    except Exception as err:
        print(str(err))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", action="store", help="IP to scan", type=str)
    parser.add_argument("sport", action="store", nargs="?", default=1, help="Starting port range", type=int)
    parser.add_argument("eport", action="store", nargs="?", default=1024, help="End port range", type=int)
    parser.add_argument("-t", "--throttle", action="store", help="throttle connection attempts",
        nargs="?", default=0.25, const=0.05)

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    main(args)