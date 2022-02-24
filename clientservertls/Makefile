all:
	@echo "Type: 'make senderserver[#1-4]' then 'make senderclient[#1-4]'"
senderserver:
	python server.py $(PORT)
senderclient:
	python client.py $(PORT)
receiverserver:
	python receiver.py $(PORT)
receiverclient:
	python rclient.py $(PORT)
senderserver2:
	python server.py 2221
senderclient2:
	python client.py 2221
receiverserver2:
	python receiver.py 3332
receiverclient2:
	python rclient.py 3332
senderserver3:
	python server.py 2220
senderclient3:
	python client.py 2220
receiverclient3:
	python receiver.py 3331
receiverserver3:
	python rclient.py 3331
senderserver4:
	python server.py 2229
senderclient4:
	python client.py 2229
receiverserver4:
	python receiver.py 3330
receiverclient4:
	python rclient.py 3330
clean:
	fuser 2222/tcp
	fuser 3333/tcp
	fuser 2221/tcp
	fuser 3332/tcp
	fuser 2220/tcp
	fuser 3331/tcp
	fuser 2229/tcp
	fuser 3330/tcp
