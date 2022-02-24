#Brandon Hudson
#CS447 Network and Data Communication
#SMTP Appication

import os
import sys
from sys import argv
import time
from datetime import datetime 
from socket import *
import select
import pathlib
import errno
import time
import threading
import pathlib
import base64
import random 
import multiprocessing
import ssl

PORT = int(argv[1])
count = 0


listen_addr = ''
listen_port = PORT
server_cert = 'server.crt'
server_key = 'server.key'
client_certs = 'client.crt'

ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ctx.verify_mode = ssl.CERT_REQUIRED
ctx.load_cert_chain(certfile=server_cert, keyfile=server_key)
ctx.load_verify_locations(cafile=client_certs)

ctx.options |= (ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2)
print(ctx.get_ca_certs())

s = socket(AF_INET, SOCK_STREAM)
s.bind((listen_addr, listen_port))
s.listen(5)




while True:

    print("Waiting for client")
    newsocket, fromaddr = s.accept()
    print("Client connected: {}:{}".format(fromaddr[0], fromaddr[1]))
    conn = ctx.wrap_socket(newsocket, server_side=True)
    print("SSL established. Peer: {}".format(conn.getpeercert()))

    cmd_Choice2 = conn.recv(1024)
    choiceDecoded2 = cmd_Choice2[1]
    conn.send(bytes("Welcome to the Server", "utf-8"))

    choice1 = conn.recv(1024)
    choiceDecoded3 = choice1.decode()
 
    #print(choiceDecoded3)
    if(choiceDecoded3.casefold() == "GET".casefold()):



        userEmail = conn.recv(1024)
        choiceDecoded3 = userEmail.decode()

        print(choiceDecoded3)

        path = "./db/" + str(choiceDecoded3) + "/"

        for path in pathlib.Path(path).iterdir():
            if path.is_file():

                f = open(str(path))
                conn.send(bytes(f.read(), "utf-8"))

                count += 1

        path = "./db/" + str(choiceDecoded3) 

        path = "./db/" + str(choiceDecoded3) + "/"

        count = 0

        files = []

        for r, d, f in os.walk(path):
            for file in f:
                if '.email' in file:
                    files.append(os.path.join(r, file))
                    count+=1
        
        for f in files:
            print(f)
            email = open(f,'r')
            conn.send(bytes(email.read(),"utf-8"))
        

        

    #print(choiceDecoded2)

    
