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
import base64
import random 
import ssl

PORT = int(argv[1])

HEADERSIZE = 10


#server_cert = 'cert.pem'
#client_cert = 'cert.pem'
#client_key = 'key.pem'



host_port = PORT
server_sni_hostname = 'vm-02.cs.siue.edu'
server_cert = 'server.crt'
client_cert = 'client.crt'
client_key = 'client.key'



#rs = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#sAddr = (socket.gethostname(), PORT)



x = 0
sender_Email = ""
recivers_Email = ""
sender_Message = ""
user_Input = ""
user_reply = ""
user_Command = ""
data = ""
has_HELO = False
has_MAILFROM = False
has_RCTPTO = False
has_DATA = False
userFOUND = False
has_AUTH = False

#hostname = socket.gethostname()


context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


hostname = socket.gethostbyname(socket.gethostname())

host_addr = hostname

#conn = ssl.wrap_socket(s, server_side=False, do_handshake_on_connect=True)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
print(context.get_ca_certs())

print(hostname)            
#print(conn.getpeercert())
print(PORT)

#conn.do_handshake()

conn.connect((host_addr, host_port))



print("CONNECTED")



cert = conn.getpeercert()
#ssl.match_hostname(cert, hostname)
print(cert)


while True:

    print("SSL established. Peer: {}".format(conn.getpeercert()))
    print("Sending: 'Hello, world!")
    conn.send(b"Hello, world!")
    print("Closing connection")

    cmdLine = input("\n Type 'Connect'")
    cmdLine_send = cmdLine.encode("utf-8")
    cmdLine_Header = f"{len(cmdLine):<{HEADERSIZE}}".encode('utf-8')
    conn.send(cmdLine_Header + cmdLine_send)

        
            
    print("\n\tList of Commands \n\t\t|HELO| \t|MAIL FROM| \t|RCTP TO| \n\t\t|DATA| \t|AUTH| \t|HELP| \t|QUIT|")

    while(user_Command != "quit"):
        user_Command = ""
        user_reply = input("\n Type a Command\n")
        user_replyEn = user_reply.encode("utf-8")
        userReply_Header = f"{len(user_reply):<{HEADERSIZE}}".encode('utf-8')
        conn.send(userReply_Header + user_replyEn)

        if(user_reply.casefold() == "HELO".casefold() or user_reply == "HELO server".casefold()):
            if(has_HELO == False):
                sender_Email = ""
                recivers_Email = ""
                sender_Message = ""
                user_Input = ""
                user_reply = ""
                user_Command = ""
                data = ""                    
                has_MAILFROM = False
                has_RCTPTO = False
                has_DATA = False

            user_reply == ""
            msg2 = conn.recv(1024)
            

            print(msg2.decode("utf-8"))
        
            has_HELO = True

        elif(user_reply.casefold() == "AUTH".casefold()):
            
            
            msg2 = conn.recv(1024)               
            print(msg2.decode("utf-8"))
            auth_username = input("\nEnter username:  ")
            auth_usernameEn = base64.b64encode(auth_username.encode("utf-8"))
            authuser_Header = f"{len(auth_username):<{HEADERSIZE}}".encode('utf-8')
            conn.send(authuser_Header + auth_usernameEn)

            if(auth_username[-8:] != "@447.edu"):
                errormsg = conn.recv(1024)
                continue

            serverReply = conn.recv(1024)
            serverreplayDecodded = serverReply.decode("utf-8")
            print(serverreplayDecodded)
            if(serverreplayDecodded.casefold().strip() == 'MATCH FOUND'.casefold().strip()):
                
                #WHAT is your password? aksed from server#
                msg2 = conn.recv(1024)               
                print(msg2.decode("utf-8"))

            
                auth_password = input("\nEnter password:  ")
                auth_passwordEn = base64.b64encode(auth_password.encode("utf-8"))
                authpassword_Header = f"{len(auth_password):<{HEADERSIZE}}".encode('utf-8')
                conn.send(authpassword_Header + auth_passwordEn)

                msg2 = conn.recv(1024)  
                authcheck = msg2.decode("utf-8")

                print(authcheck)

                if(authcheck.casefold() == "Auth=TRUE".casefold()):
                    has_AUTH = True
                    print("AUTH HERE!!")
                    msg2 = conn.recv(1024)               
                    print(msg2.decode("utf-8"))



            else:

                msg2 = conn.recv(8192)               
                print(msg2.decode("utf-8"))
                conn.close()
                sys.exit(1)
            
        elif(user_reply.casefold() == "MAIL FROM".casefold()):

            if(has_MAILFROM == True):
                print("You have overwritten previouslys entered email. Re-enter your email")

            if(has_HELO == False):
                print("Status Code: 503 - Rude clients do not get serverd")
            elif(has_AUTH == False):
                print("Status Code: 432 - Need to AUTH before using server")
            else:
                if(has_HELO != True):
                    print("Status code: 503 - Bad sequence of commands")
                elif(has_AUTH != True):
                    print("Status Code: 503 - Need to AUTH before using server")
                else:         
                    user_reply == ""
                    msg2 = conn.recv(1024)
                    print(msg2.decode("utf-8"))
                    uemail = input("'@447.edu' has to be included\n")

                    

                                        
                    sender_EmailEn = uemail.encode("utf-8")
                    uemail_Header = f"{len(uemail):<{HEADERSIZE}}".encode('utf-8')
                    conn.send(uemail_Header + sender_EmailEn)
                    if(uemail[-8:] != "@447.edu"):
                        msg2 = conn.recv(1024)
                        print(msg2.decode("utf-8"))
                        continue
                    has_MAILFROM = True

        elif(user_reply.casefold() == "RCTP TO".casefold()):

            if(has_RCTPTO == True):
                print("You have overwritten previously entered email. Re-enter the email")

            if(has_HELO == False):
                print("Status Code: 503 - Rude clients do not get serverd")
            elif(has_AUTH == False):
                print("Status Code: 503 - Need to AUTH before using server")
            elif(has_MAILFROM == False):
                print("Status Code: 503 - You need to first provide your email\n")    
            else:
                if(has_HELO != True and has_MAILFROM == True):
                    print("Status code: 503 - Bad sequence of commands")
                else: 
                    user_reply == ""
                    msg2 = ""#test This
                    msg2 = conn.recv(1024)
                    print(msg2.decode("utf-8"))
                    recivers_Email = input("'@447.edu' will be added. Do not include when entered\n")
                    
                    recivers_EmailEn = recivers_Email.encode("utf-8")
                    remail_Header = f"{len(recivers_Email):<{HEADERSIZE}}".encode('utf-8')
                    conn.send(remail_Header + recivers_EmailEn)

                    msg3 = conn.recv(1024)
                    print(msg3.decode("utf-8"))

                    eSubject = input("")

                    email_subEn = eSubject.encode("utf-8") 
                    emailSub_Header = f"{len(eSubject):<{HEADERSIZE}}".encode('utf-8')
                    conn.send(emailSub_Header + email_subEn)

                    has_RCTPTO = True

        elif(user_reply.casefold() == "DATA".casefold()):
            if(has_HELO == False):
                print("Status Code: 503 - Rude clients do not get serverd")
            elif(has_AUTH == False):
                print("Status Code: 503 - Need to AUTH before using server")
            elif(has_MAILFROM == False):
                print("Status Code: 503 - You need to first provide your email\n") 
            elif(has_RCTPTO == False):
                print("Status Code: 503 - You need to provide recivers' email ")        
            else:
                if(has_HELO != True and has_MAILFROM == True and has_RCTPTO == True):
                    print("Status code: 503 - Bad sequence of commands")
                else:        
                    user_reply == ""
                    msg2 = ""#test This
                    msg2 = conn.recv(1024)
                    print(msg2.decode("utf-8"))
                    data = input("What is  your message?\n")
                    
                    dataEn = data.encode("utf-8")
                    data_Header = f"{len(data):<{HEADERSIZE}}".encode('utf-8')
                    conn.send(data_Header + dataEn)
                    has_DATA = True
                    print("Status Code: 250 - Mail was sent")

                    sender_Email = ""
                    recivers_Email = ""
                    sender_Message = ""
                    user_Input = ""
                    user_reply = ""
                    user_Command = ""
                    data = ""
        elif(user_reply.casefold() == "HELP".casefold()):
            print("\n Commands have to be enter in correct order which is[command are space sensitive and wont be reconized with space on either side]: HELO, MAIL FROM, RCTP TO, DATA")

        elif(user_reply.casefold() == "quit".casefold()):
            sys.exit()    
        elif(user_reply == "" or user_reply == " "):
            
            user_reply = input("\n Type a Command\n")
            user_replyEn = user_reply.encode("utf-8")
            userReply_Header = f"{len(user_reply):<{HEADERSIZE}}".encode('utf-8')
            conn.send(userReply_Header + user_replyEn)
                
        else:
            print("Status code: 500 - Command isn't reconized")
    else:
        print("Status code: 503 - Bad sequence of commands")     




