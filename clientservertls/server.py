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
import threading
import pathlib
import base64
import random 
import multiprocessing
import ssl


# PEM PASSWORD IS: cs447



THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))    

PORT = int(argv[1])

filePath = "./db/"
filePath = (filePath)

lock = multiprocessing.Lock()

if not os.path.exists(filePath):               
    os.mkdir("db")

def helo_smtp():
    os.write(1, 'helo server\n'.encode("utf-8"))
    
    sys.stdout.write('helo server2\n')    


''' TCP '''
HEADERSIZE = 10
user_Email = ""
sender_Email = ""
recivers_Email = ""
msgdata = ""
email_Subject = ""
emailSub_Decoded = ""
msgDecoded = ""
recpt_Email = ""
userpassFile = ""
userPassword = ""
newuserPassword = ""
has_HELO = False
has_MAILFROM = False
has_RCTPTO = False
has_DATA = False
has_AUTHCheck = False
encodedUsernameMatch = False
connection_time = 0
time_update = 0
time_check = 0
emailCount = 0
count = 0
threadCount = 0
threadArr = []
time = time

listen_addr = ''
listen_port = PORT
server_cert = 'server.crt'
server_key = 'server.key'
client_certs = 'client.crt'







    

#socket.getaddrinfo()

ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ctx.verify_mode = ssl.CERT_REQUIRED
ctx.load_cert_chain(certfile=server_cert, keyfile=server_key)
ctx.load_verify_locations(cafile=client_certs)

ctx.options |= (ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2)

if ssl.HAS_TLSv1_3:
    print("{0} with support for TLS 1.3".format(ssl.OPENSSL_VERSION))

print(ctx.get_ca_certs())


#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s = socket.socket()
    s.bind((listen_addr, listen_port))
    s.listen(5)
except Exception as e:
    raise e



def writeEmail(userEmail, recptEmail, msgData):
    lock.acquire()
    filePath = (("./db/" + userEmail + "/" + str(count) + "s"  + ".email"))

    with open(filePath, 'a') as f:
        f.write(" Message: \n\t" + msgData)
        f.close()
    
    filePath = (("./db/" + recptEmail + "/" + str(count) + ".email"))

    with open(filePath, 'a') as f:
        f.write(" Message: \n\t" + msgData)
        f.close()

    f.close()
    
    #time.sleep(5)
    lock.release()

def authuser(userID, password, path):
    lock.acquire()
    
    with open(path, 'a+b') as f:

        f.write(userID)
        f.write("\n".encode("utf-8"))
        f.write(password)
        f.write("\n".encode("utf-8"))
        
    print("FILE:\n")
    with open("./db/.user_pass", 'r+') as f:
        userpassFile = f.read()
        #f.close()

    print("FILE END\n")
    
    #time.sleep(5)
    lock.release()

def checkNewUser(client, check, user, path):
    lock.acquire()
    fullEncyptedUserID = base64.b64encode(user.encode("utf-8"))
    print(fullEncyptedUserID)

    if not os.path.exists("./db/.user_pass"):
        with open("./db/.user_pass", 'w') as f:
            f.write("Usernames and Passwords encoded\n")

                        
    with open(path, 'r') as f:
        has_AUTHCheck = False
        while True:
            userSerarch = True
            
            userFile = f.readline()
            #print(userFile)
            
            if userFile == "": 
                print("End of File")
                userSerarch = False
                break
            encodedUser = base64.b64encode(user.encode("utf-8"))

            string1 = str(encodedUser.decode())
            string2 = str(userFile)


            print(string1)
            
            print(string2)

            print(string1.lower().strip() == string2.lower().strip())

            if  string1.lower().strip() == string2.lower().strip():
                
                client.send(bytes("MATCH FOUND", "utf-8"))
                client.send(bytes("What is your password?", "utf-8"))
               
                userPassEn  = client.recv(1024)
                userpassDecoded = userPassEn.decode("utf-8")[10:]

                print(userpassDecoded)
 
                passwordString = str(userpassDecoded).encode("utf-8")
                passwordStringEn = base64.b64encode(passwordString)
                print("\n")
                print("\n")

                print(passwordStringEn.decode("utf-8"))
                passwordLine = f.readline().strip()
                print(passwordLine)

                if(userpassDecoded == passwordLine):
                    print("Password Match!! " + passwordLine)
                    has_AUTHCheck = True
                    userSerarch = False
                    client.send(bytes("Auth=TRUE", "utf-8"))
                    

                check = True
                encodedUsernameMatch = True
                print("USER FOUND")
                break
                
    if(userSerarch == False and has_AUTHCheck == False):
        newuserPassword = str(random.randrange(10000, 99999)) + "447"
        print(newuserPassword)
       
        fullEncyptedPassword = base64.b64encode(newuserPassword.encode("utf-8"))
        fullEncyptedPUsername = base64.b64encode(user.encode("utf-8"))

        #lock.acquire()
    
        with open(path, 'a+b') as f:

            f.write(fullEncyptedPUsername)
            f.write("\n".encode("utf-8"))
            f.write(fullEncyptedPassword)
            f.write("\n".encode("utf-8"))
            
        print("FILE:\n")
        with open("./db/.user_pass", 'r+') as f:
            userpassFile = f.read()
            #f.close()
            
        #print(userpassFile)
        print("FILE END\n")
        
        #time.sleep(5)
        #lock.release()

        client.send(bytes("\nThis is your password: " + newuserPassword + "\nReconnect and enter your password", "utf-8"))

        #t3 = threading.Thread(target=authuser, args=(user, fullEncyptedPassword, filePath))
        
        #t3.start()                  
        #t3.join()

        client.close()
    else:
        has_AUTHCheck = True
        client.send(bytes("THIS PART", "utf-8"))
        

    #time.sleep(5)
    lock.release()

def deal_with_client(connstream):
    data = connstream.recv(1024)
    while data:
        if data == None:            
            break
        #data = connstream.recv(1024)
        return data

def new_client(certi, client, connection):  

    if not os.path.exists("./db/.server_log"):
        with open("./db/.server_log", 'w') as f:
            f.write("Server Log\n")

    print("NEW CONNECTION |{connection[0]}| EMERGES! Port:|{connection[1]}|")

    #tls_in_buff = ssl.MemoryBIO()
    #tls_out_buff = ssl.MemoryBIO()

    #tls_obj = ctx.wrap_bio(tls_in_buff, tls_out_buff, server_side=True)

    data = client.recv(4096)

    print(data.decode())

    
    data = client.recv(1024)
    print(data.decode())
             
    while(True):
       
  
        cmd_Choice2 = client.recv(1024)
        choiceDecoded2 = cmd_Choice2.decode()[10:]
        print(choiceDecoded2)


        #with open("./db/.server_log", 'a') as f:
            #f.write("timestamp from -" + str(s.getsockname()) + " to -" + str(client.getsockname()) + "-command" +  choiceDecoded2 + "\n")

        if(choiceDecoded2.casefold() == "CLOSE".casefold()):
            client.close()
        if(choiceDecoded2.casefold() == "HELO".casefold()):            
            client.send(bytes("Welcome to the server\n", "utf-8"))
            has_HELO = True

        elif(choiceDecoded2.casefold()  == "AUTH".casefold()):
            client.send(bytes("\nWhat is your username?" ,"utf-8"))

            authusernameEn = client.recv(1024)
            authusernameDecoded =  authusernameEn.decode()[10:]
 
            decodedusrname = base64.b64decode(authusernameDecoded)


            #with open("./db/.server_log", 'a') as f:
                #f.write("timestamp from -" + str(s.getsockname()) + " to -" + str(client.getsockname()) + "-command: AUTH " +  str(authusernameDecoded) + "\n")

            sufix = authusernameDecoded[-8:]

            print(sufix)   
            print(decodedusrname[-8:].decode("utf-8"))    
                    
            if(decodedusrname[-8:].decode("utf-8") != "@447.edu"):
                client.send(bytes("Email format is wrong","utf-8"))
                with open("./db/.server_log", 'a') as f:
                    f.write("timestamp from -" + str(s.getsockname()) + " to -" +str(client.getsockname()) + "-command: ERROR AUTH " +  str(authusernameDecoded) + "\n")
                continue

            filePath = "./db/.user_pass"

            encodedUsernameMatch = False
            t2 = threading.Thread(target=checkNewUser, args=(client, encodedUsernameMatch, authusernameDecoded, filePath))
            t2.start()
            t2.join()

            has_AUTHCheck = True

            print(userpassFile)

        elif(choiceDecoded2.casefold() == "MAIL FROM".casefold()):
            print(has_AUTHCheck)
            
            if(has_HELO == False):
                print("Status Code: 503 - Rude clients do not get serverd")
            elif(has_AUTHCheck == False):
                print("Status Code: 432 - You need to first AUTH\n")  


            else:  
                client.send(bytes("What is your email username?", "utf-8"))
                    
                sender_Email = client.recv(1024)
                senderEmail_Decoded = sender_Email.decode("utf-8")[10:]           
                user_Email = senderEmail_Decoded      

                with open("./db/.server_log", 'a') as f:
                    f.write("timestamp from -" + str(s.getsockname()) + " to -" + str(client.getsockname()) + "-command: MAIL FROM " +  user_Email + "\n")

                sufix = user_Email[-8:]

                print(sufix)       
                
                if(user_Email[-8:] != "@447.edu"):
                    client.send(bytes("Email format is wrong","utf-8"))
                    with open("./db/.server_log", 'a') as f:
                        f.write("timestamp from -" + str(s.getsockname()) + " to -" + str(client.getsockname()) + "-command:ERROR MAIL FROM " +  user_Email + "\n")
                    continue  
                    
                print('Mail from:' + user_Email )

                filePath = ("./db/" + user_Email)

                if not os.path.exists(filePath):
                    os.mkdir(filePath)

                has_MAILFROM = True    

        elif(choiceDecoded2.casefold()  == "RCTP TO".casefold()):

                if(has_HELO == False):
                    print("Status Code: 503 - Rude clients do not get serverd")
                elif(has_AUTHCheck == False):
                    print("Status Code: 503 - You need to first AUTH\n") 
                elif(has_MAILFROM == False):
                    print("Status Code: 503 - You need to first provide your email\n")  

                else:
                    client.send(bytes("What is the receivers email?", "utf-8"))
                        
                    recivers_Email = client.recv(1024)
                    reciversEmail_Decoded = recivers_Email.decode("utf-8")[10:]            
                    recpt_Email = reciversEmail_Decoded      

                    client.send(bytes("What is the email subject title?", "utf-8"))
                        
                    email_Subject = client.recv(1024)
                    emailSub_Decoded = email_Subject.decode("utf-8")[10:]    

                    filePath = ((THIS_FOLDER + "/db/" + user_Email + "/" ))
                    if not os.path.exists(filePath):
                        os.makedirs(filePath)

                    filePath = ((THIS_FOLDER + "/db/" + recpt_Email + "/" ))
                    if not os.path.exists(filePath):
                        os.makedirs(filePath)

                    filePath = ((THIS_FOLDER + "/db/" + recpt_Email.lower() + "/"))
   
                    for path in pathlib.Path(filePath).iterdir():
                        if path.is_file():
                            count += 1

                            print(count)
                    
                    date1 = datetime.now()
                    year = date1.strftime("%Y")
                    month = date1.strftime("%m")
                    day = date1.strftime("%d")
                    time = date1.strftime("%H:%M:%S")

                    date = month + "/" + day + "/" + year

                    filePath = ((THIS_FOLDER + "/db/" + user_Email.lower() + "/"))
                    count = 0
   
                    for path in pathlib.Path(filePath).iterdir():
                        if path.is_file():
                            count += 1

                            print(count)

                    fullpathname = os.path.join("./db/" + user_Email + "/" , str(count)  + "s" + ".email")
                    
                    print('To:' + recpt_Email + "@447.edu")
                    with open( fullpathname, 'w') as fn:
                        fn.write("\n\t\t\t\t------------------\n")
                        fn.write("\t\t\t\t|DATE: " + date + "|\t|TIME: " + time + "|")
                        fn.write("\n\t\t\t\t------------------\n")
                        fn.write("\n\t\t\t\t\t\t\t -----------")
                        fn.write("\n\t\t\t\t\t\t\t [Delivered]")
                        fn.write("\n\t\t\t\t\t\t\t -----------\n")
                        fn.write("\tMAIL FROM: " + user_Email +  "@447.edu" +"\n")
                        fn.write("\tRCTP TO: " + recpt_Email + "@447.edu"+"\n")
                        fn.write("\tSubject:" + emailSub_Decoded + '\n\n')
                    
                    filePath = ((THIS_FOLDER + "/db/" + recpt_Email.lower() + "/"))
                    count = 0
   
                    for path in pathlib.Path(filePath).iterdir():
                        if path.is_file():
                            count += 1

                            print(count)
   
                    fullpathname2 = os.path.join("./db/" + recpt_Email + "/", str(count) + ".email")

                    print('To:' + recpt_Email + "@447.edu")
                    with open(fullpathname2, 'w') as f:
                        f.write("\t\t\t\t|DATE: " + date + "|\t|TIME: " + time + "|")
                        f.write("\n\t\t\t\t\t\t\t --------")
                        f.write("\n\t\t\t\t\t\t\t [Received]")
                        f.write("\n\t\t\t\t\t\t\t --------\n")
                        f.write("\tMAIL FROM: " + user_Email +  "@447.edu" + "\n")
                        f.write("\tRCTP TO: " + recpt_Email  +  "@447.edu" + "\n")
                        f.write("\tSubject:" + emailSub_Decoded + '\n\n')

                    has_RCTPTO = True

        elif(choiceDecoded2.casefold() == "DATA".casefold()):
            if(has_HELO == False):
                print("Status Code: 503 - Rude clients do not get serverd")
            elif(has_MAILFROM == False):
                print("Status Code: 503 - You need to first provide your email\n") 
            elif(has_RCTPTO == False):
                print("Status Code: 503 - You need to provide recivers' email ")   

            else:
                if(has_HELO != True and has_MAILFROM == True and has_RCTPTO == True):
                    print("Status code: 503 - Bad sequence of commands")

                else: 
                    client.send(bytes("What is the meaasge you want to send?", "utf-8"))
                        
                    msgdata = client.recv(4096)
                    msgdata_Decoded = msgdata.decode("utf-8")[10:]
                    #print("FROM: " + senderEmail_Decoded)
                    msgDecoded = msgdata_Decoded     
                    has_DATA = True    
                    
                    print('Message:\n' + msgDecoded)
                    t4 = threading.Thread(target=writeEmail, args=(user_Email, recpt_Email, msgDecoded))
                    
                    t4.start()
                    t4.join()

                    user_Email = ""
                    sender_Email = ""
                    recivers_Email = ""
                    msgdata = ""
                    email_Subject = ""                        
                    has_MAILFROM = False
                    has_RCTPTO = False
                    has_DATA = False



while True:
    print("Waiting for client")
    newsocket, fromaddr = s.accept()
    print("Client connected: {}:{}".format(fromaddr[0], fromaddr[1]))
    conn = ctx.wrap_socket(newsocket, server_side=True)
    print("SSL established. Peer: {}".format(conn.getpeercert()))
    buf = b''  # Buffer to hold received client data

    cert = "Cert"
    t1 = threading.Thread(target=new_client, args=(cert, conn, fromaddr))
    
    t1.start()
    t1.join()

    try:
        while True:
            data = conn.recv(4096)
            if data:
                # Client sent us data. Append to buffer
                buf += data
            else:
                # No more data from client. Show buffer and close connection.
                print("Received:", buf)
                break
    finally:
        print("Closing connection")
        conn.shutdown(socket.SHUT_RDWR)


        conn.close()




    print((f"Connextion" , " has been established!!"))
    os.system('python --version')

    if ssl.HAS_TLSv1_3:
        print("{0} with support for TLS 1.3".format(ssl.OPENSSL_VERSION))
        
    #port = s.getsockname()
   # print(port)
     


