#! /usr/bin/#!/usr/bin/env python
import socket
import subprocess
import sys
import os
from datetime import datetime

#Clear the screen
subprocess.call('clear', shell=True)

#Assign protocols
proto = socket.getprotobyname('tcp')
imcp = socket.getprotobyname('icmp')
udp = socket.getprotobyname('udp')

#Check for in-line args
hostlist = [h for h in sys.argv[1:]]
if hostlist:
    print hostlist

if not hostlist:
    print "hostlist is empty"
#If there are not user given hosts when the program starts, ask for host
    remoteServer = raw_input("Enter a remote host to scan: ")
    if remoteServer.isalpha():
        remoteServerIP = socket.gethostbyname(remoteServer)
        hostlist.append(remoteServerIP)
    else:
        remoteServerIP= socket.gethostbyaddr(remoteServer)[2][0]
        hostlist.append(remoteServerIP)

    print hostlist

#Ask for port
portInput = raw_input("Enter the port (##) or range of ports (##-##) to be scanned: ")
if "-" in portInput:
    port1 = int(portInput.split("-")[0])
    port2 = int(portInput.split("-")[1]) + 1
else:
    port1 = int(portInput)
    port2 = int(portInput) + 1
    # port2 = portInput

#Ask which protocol should be used
protoName = "TCP"

protoGet = raw_input("Which protocol? (1)TCP (2)UDP (3)ICMP: ")
if protoGet == '2':
    print "here"
    proto = udp
    protoName = "UDP"
elif protoGet == '3':
    proto = imcp
    protoName = "IMCP"

for host in hostlist:
#Print a nice banner with information on which host we are about to scan
    print "-" * 80
    print "Please wait, scanning remote host", host , " with ", protoName, " protocol"
    print "-" * 80

    #Check what time the scan started
    t1 = datetime.now()

    #Using the range function to specify ports (here it will scan all borts btwn 1 - 1024)

    #We also put in some error handling for catching errors

    try:
        for port in range (port1,port2):

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)

            result = sock.connect_ex((host, port))

            if result == 0:
                print "Port {}: Open".format(port)
                sock.close()

    except KeyboardInterrupt:
        print "You pressed Ctrl+C"
        sys.exit()

    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'
        sys.exit()

    except socket.error:
        print "Couldn't connect to server"
        sys.exit()


    #Checking the time agin
    t2 = datetime.now()

    #calculate the total datetime
    total = t2-t1

    #Printing the time to screen
    print 'Scan completed in: ', total


    #Run Traceroute on the host
    print "-" * 40
    print "Traceroute"
    print "-" * 40
    os.system("traceroute {}".format(host))
    print "*" * 120
















#{Worked through tutorial @ https://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python}
