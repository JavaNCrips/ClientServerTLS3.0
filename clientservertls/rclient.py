
#Brandon Hudson
#CS447 Network and Data Communication
#SMTP Appication

import os
import sys
from sys import argv
import time
from datetime import datetime 
import socket
import select
import errno
import time
import ssl

PORT = int(argv[1])

HEADERSIZE = 10

host_port = PORT
server_sni_hostname = 'vm-02.cs.siue.edu'
server_cert = 'server.crt'
client_cert = 'client.crt'
client_key = 'client.key'

#rs = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)
rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


hostname = socket.gethostbyname(socket.gethostname())
host_addr = hostname

conn = context.wrap_socket(rs, server_side=False, server_hostname=server_sni_hostname)
print(context.get_ca_certs())

print(hostname)            

print(PORT)



conn.connect((host_addr, host_port))


sAddr = (socket.gethostname(), PORT)

conn.send(bytes("CLIENT-Receiver","utf-8"))

msg = conn.recv(1024)
print(msg.decode())



while True:
    

    rin = input("what do you want to do? [GET] to open emails or [Exit] to close connection to server")

    conn.send(bytes(rin,"utf-8"))



    if(rin.casefold() == "GET".casefold()):
        print("Open")
        rin = input("\nEnter Email: ")
        #rs.sendto(rin.encode("utf-8"), sAddr)
        conn.send(bytes(rin,"utf-8"))
        msg = conn.recv(8196)
        print(msg.decode())

    if(rin.casefold() == "AUTH".casefold()):
        print("AUTHintcation")
        #rs.sendto(rin.encode("utf-8"), sAddr)
        conn.send(bytes(rin,"utf-8"))

    elif(rin.casefold() == "Exit".casefold()):
        print("Exiting...")
        conn.close()
        sys.exit(1)