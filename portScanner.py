#!/usr/bin/python -tt
import socket
import threading
from queue import Queue
import os
import argparse
import time
import sys
from termcolor import cprint
from pyfiglet import figlet_format
import random


class style():
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RESET = '\033[0m'
    MAGENTA = '\033[35m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[37m'
    VOILET = '\33[36m'
    BOLD = '\033[1m'


start_time = time.time()

colors = [style.RED, style.GREEN, style.BLUE,
          style.YELLOW, style.MAGENTA, style.VOILET, style.WHITE]


def get_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threads", dest="threads",
                        help="Specify Threads(Default 600 (MAX - 849))")
    parser.add_argument("-ip", "--host", dest="host",
                        help="Specify Host IP address")
    parser.add_argument("-s", "--start_port", dest="start",
                        help="Specify Starting Port Number(Default 1)")
    parser.add_argument("-e", "--end_port", dest="end",
                        help="Specify Ending Port Number(Default 65535)")
    options = parser.parse_args()

    if not options.host:
        parser.error("[+] Specify an IP Address Of Host To Scan --help for more details")

    return options


def portmapper():
    cprint(figlet_format('PORTMAPPER', font='standard'), 'red', attrs=['bold'])


arg = get_arg()
host = arg.host
threads = arg.threads
start = arg.start
end = arg.end

os.system("clear")

portmapper()

queue = Queue()
open_ports = []


def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        sock.connect((host, port))
        if port:
            print("\r"+random.choice(colors) +
                  "Scanning Port Number - "+str(port), end="")
            return True
    except:
        if port:
            print("\r"+random.choice(colors) +
                  "Scanning Port Number - "+str(port), end="")
        return False


def fill_queue(port_list):
    for port in port_list:
        queue.put(port)


def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            open_ports.append(port)


if start and end == None:
    port_list = range(int(start), 65535)
elif start and end:
    port_list = range(int(start), int(end))
elif end and start == None:
    port_list = range(1, int(end))
else:
    port_list = range(1, 65535)

fill_queue(port_list)

thread_list = []

if start and end == None:
    print("\nScanning Port From "+start+" To 65535\n")
    Total_ports = 65535-int(start)
    print("\nTotal Ports To Scan -", str(Total_ports), "\n")
elif start and end:
    print("\nScanning Port From "+start+" To "+end+"\n")
    Total_ports = int(end)-int(start)
    print("\nTotal Ports To Scan -", str(Total_ports), "\n")
elif end and start == None:
    print("\nScanning Port From 1 To "+end+"\n")
    Total_ports = int(end)
    print("\nTotal Ports To Scan -", str(end), "\n")
else:
    print("\nScanning Port From 1 To 65535\n")
    Total_ports = int(65535)
    print("\nTotal Ports To Scan - 65535\n")

if threads:
    if int(threads) < 850:
        print("\n[+] Using "+threads+" Threads\n\n")
        for t in range(int(threads)):
            thread = threading.Thread(target=worker)
            thread_list.append(thread)
    if int(threads) > 849:
        print("\n[+] Using 849 Threads(MAX)\n\n")
        for t in range(849):
            thread = threading.Thread(target=worker)
            thread_list.append(thread)
else:
    print("\n[+] Using 600 Threads\n\n")
    for t in range(600):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()
os.system("clear")
portmapper()
print("-"*50)
print("|S.NO\t|\tOPEN PORTS  |   Assigned Service |")
print("-"*50+"\n")
count = 1
for single_port in open_ports:
    if single_port == 20:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\r\t\t\tftp")
    elif single_port == 21:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tftp")
    elif single_port == 22:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tssh")
    elif single_port == 23:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\telnet")
    elif single_port == 25:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tsmtp")
    elif single_port == 26:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\trsftp")
    elif single_port == 53:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tdns")
    elif single_port == 67:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tdhcp")
    elif single_port == 68:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tdhcp")
    elif single_port == 69:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\ttftp")
    elif single_port == 80:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\thttp")
    elif single_port == 110:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tpop3")
    elif single_port == 111:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\trpc")
    elif single_port == 119:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tnntp")
    elif single_port == 123:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tntp")
    elif single_port == 139:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port) +
              "\r\t\t\t\tsmb/samba or netbios-ssn")
    elif single_port == 143:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\timap")
    elif single_port == 161:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tsnmp")
    elif single_port == 194:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tirc")
    elif single_port == 389:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tldap")
    elif single_port == 443:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\thttps")
    elif single_port == 445:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port) +
              "\r\t\t\t\tsmb/samba or microsoft-ds")
    elif single_port == 512:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\texec")
    elif single_port == 513:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tlogin")
    elif single_port == 514:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tshell")
    elif single_port == 993:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\timaps")
    elif single_port == 1099:
        print(" P.NO", str(count)+"\r\t\t" +
              str(single_port)+"\r\t\t\t\trmiregistry")
    elif single_port == 1524:
        print(" P.NO", str(count)+"\r\t\t" +
              str(single_port)+"\r\t\t\t\tingreslock")
    elif single_port == 1812:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tradius")
    elif single_port == 2049:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tnfs")
    elif single_port == 2121:
        print(" P.NO", str(count)+"\r\t\t" +
              str(single_port)+"\r\t\t\t\tccproxy-ftp")
    elif single_port == 3306:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tmysql")
    elif single_port == 3632:
        print(" P.NO", str(count)+"\r\t\t" +
              str(single_port)+"\r\t\t\t\tdistccd")
    elif single_port == 5432:
        print(" P.NO", str(count)+"\r\t\t" +
              str(single_port)+"\r\t\t\t\tpostgresql")
    elif single_port == 5900:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tvnc")
    elif single_port == 6000:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tx11")
    elif single_port == 6667:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tirc")
    elif single_port == 6697:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tircu-s")
    elif single_port == 7547:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tcwmp")
    elif single_port == 7547:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tcwmp")
    elif single_port == 8009:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\tajp13")
    elif single_port == 8080:
        print(" P.NO", str(count)+"\r\t\t"+str(single_port)+"\r\t\t\t\thttp")
    elif single_port == 8787:
        print(" P.NO", str(count)+"\r\t\t" +
              str(single_port)+"\r\t\t\t\tmsgsrvr")
    elif single_port == 18182:
        print(" P.NO", str(count)+"\r\t\t" +
              str(single_port)+"\r\t\t\t\topsec-ufp")
    else:
        print(" P.NO", str(count)+"\r\t\t" +
              str(single_port)+"\r\t\t\t\tunassigned")
    count += 1

end_time = time.time()

print("\nTime Taken -", str(round(end_time - start_time, 1)),
      "Seconds", "\n"+style.RESET)
