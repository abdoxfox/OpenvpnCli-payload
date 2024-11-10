import socket
import select 
import os
from fcntl import ioctl
import struct
import re
import configparser
import logging


logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
configfile = "settings.ini"
def conf():
		config = configparser.ConfigParser()
		try:
			config.read_file(open(configfile))
		except Exception as e:
			logging.getLogger().error("File %s  not Exists ",configfile)
			raise Exception(f"File {configfile}  not Exists  ")
		return config
		
def getpayload(config):
		payload = config['Config']['payload']
		return payload
			
def proxy(config):
	    proxyhost = config['Config']['proxyip']
	    proxyport = int(config['Config']['proxyport'])
	    return (proxyhost,proxyport)
	    


def tunneling(server,client):
    while True:
    	    r,_,x = select.select([server,client],[],[server,client],3)
    	    client.settimeout(3)
    	    if r:
    	        try:
    	            
        	        data= r[0].recv(2048)
        	        dataDecoded = data.decode("utf-8","ignore").split("\r\n")[0]
        	        if re.match(r'HTTP/\d(\.\d)? ',dataDecoded):
        	            print(f"\nresponse : {dataDecoded}")
        	        if r[0] is server:
        	            client.send(data)
        	        else:
        	            server.send(data)
    	        except Exception as e:
        	        logging.debug(e.args)
        	        server.close()
        	        client.close()
        	        break
    	    
    
def payloadformating(payload,host_port):
		host,port = host_port[0],str(host_port[1])
	
		payload = payload.replace('[crlf]','\r\n')
		payload = payload.replace('[crlf*2]','\r\n\r\n')
		payload = payload.replace('[cr]','\r')
		payload = payload.replace('[lf]','\n')
		payload = payload.replace('[protocol]','HTTP/1.0')
		payload = payload.replace('[ua]','Mozilla/5.0 (Linux; Android 10; M2006C3MG Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36')  
		payload = payload.replace('[raw]',f'CONNECT {host}:{port} HTTP/1.0\r\n\r\n')
		payload = payload.replace('[real_raw]',f'CONNECT {host}:{port} HTTP/1.0\r\n\r\n') 
		payload = payload.replace('[netData]',f'CONNECT {host}:{port} HTTP/1.0')
		payload = payload.replace('[realData]',f'CONNECT {host}:{port} HTTP/1.0')  	
		payload = payload.replace('[split_delay]','[delay_split]')
		payload = payload.replace('[split_instant]','[instant_split]')
		payload = payload.replace('[method]','CONNECT')
		payload = payload.replace('[ssh]',f'{host}:{port}')
		payload = payload.replace('[lfcr]','\n\r')
		payload = payload.replace('[host_port]',f'{host}:{port}')
		payload = payload.replace('[host]',host)
		payload = payload.replace('[port]',port)
		payload = payload.replace('[auth]','')
		payload = payload.replace('[split]' ,'=1.0=')
		payload = payload.replace('[delay_split]'  ,'=1.5=')
		payload = payload.replace('[instant_split]','=0.1=')
		payload = payload.replace("\\r","\r")
		payload = payload.replace("\\n","\n")
		return payload
		
	
proxy = proxy(conf())
sock = socket.create_server(("",8889),family=socket.AF_INET6, dualstack_ipv6=True)

while True :
	sock2= socket.socket()
	sock2.settimeout(3)
	cl,ad = sock.accept()
	cl.settimeout(3)
	data_rcv = cl.recv(1024).decode("utf-8","ignore").split("\r\n")[0].split(" ")[1]
	host_port = (data_rcv.split(":")[0],data_rcv.split(":")[1])
	print(host_port)
	payload = payloadformating(getpayload(conf()),host_port)
	print(f"sending payload : {payload.encode()}")
	sock2.connect((proxy))
	sock2.send(payload.encode())
	tunneling(sock2,cl)
	
	
	
	

	
