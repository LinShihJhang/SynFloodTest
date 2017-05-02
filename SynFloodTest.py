import socket  
import threading 
import time

socket.setdefaulttimeout(3)


def portTest(ip,port):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result=s.connect_ex((ip,port))
    if (result == 0 ):
        print(str(port)+" 開放")
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
    print("掃描結束")

portScan("163.13.127.236")
        





