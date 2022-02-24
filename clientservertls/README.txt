For full instrunction about how to run the program read the report inside this same folder labled "Report.txt". For a quick start type "make senderserver PORT=9000"  in 1 terminal.
It will prompt you to enter a password. The password is "cs447". This is the password for all certificates. Open another terminal and type "make senderclient PORT=9000" and type the password.
Follow thru the prompt. Type "Connect" to connect and then you will be prompted with a menu. You must use command HELO before using any other command. After HELO you must use 
AUTH to authenticate your user email. If new user you will be given a password ending in "447". You MUST reconnect both client and server to a NEW PORT to this by typing. 
"make senderserver PORT=9001" for server and "make senderclient PORT=9001" for client and typed the same password for each. Go thru the same steps as before and when AUTH enter your same email and password that was given to you.
Follow the order of command for SMTP (MAIL FROM, RCTP TO, DATA). 

To retrive emails type "receiverserver PORT=9100" for server and "receiverclient PORT=9100" for client. and follow thru the prompt.


Name:Brandon Hudson
Date: 30 June 2020
Type: Python
Details: This a a STMP sender and receiver with TLSv1.3 and base64 authenication. Creates hidden files for user passwords and log. Also creates a db folder of users. 