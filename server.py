import socket, select, sys
import subprocess
import threading
from queue import Queue


class MessageItem:
	def __init__(self, sock, msg):
		self.sock = sock
		self.msg = msg
		
		
class Server(object):
	client = 0
	#dictionary to store address corresponding to username
	record={}
	#Frame Buffer: An data structure with a queue structure for storing incoming packets.
	message_frame = Queue(maxsize = 100)
	# List to keep track of socket descriptors
	connected_list = []
	threads = []
	
	#Function to send message to connected clients by using Thread
	def send_to_all (self, server_socket):
		#Message not forwarded to server and sender itself
		print('send to all')
		while 1:
			while (self.message_frame.empty() == False):
				MessageItem = self.message_frame.get()
				sock = MessageItem.sock
				msg = MessageItem.msg
				for socket in self.connected_list:
					if socket != server_socket and socket != sock :
						try :
							#dispatching message to users
							socket.send(msg.encode())
						except :
							# if connection not available
							socket.close()
							self.connected_list.remove(socket)
							
	#Function to receive message from connected clients by using Thread
	def handle_client(self, sock, addr):
		print(f"[NEW CONNECTION] {addr} connected.")
		connected = True
		
		while connected:
			try:
				#print (connected_list)
				#print (sock)
				buffer = 4096
				data1 = sock.recv(buffer)
				data1 = data1.decode("utf-8")
				#print "sock is: ",sock
				data=data1[:data1.index("\n")]
				print ("\ndata received: ",data)
	    
	    			#get addr of client sending the message
				i,p=sock.getpeername()
				if data == "bye":
					msg="\r\33[1m"+"\33[31m "+self.record[(i,p)]+" left the conversation \33[0m\n"
					msgitem = MessageItem(sock,msg)
					self.message_frame.put(msgitem)
					
				
					print ("Client (%s, %s) is offline" % (i,p)," [",self.record[(i,p)],"]")
					del self.record[(i,p)]
					self.connected_list.remove(sock)
					sock.close()
					connected = False
					self.client = self.client - 1


				else:
					msg="\r\33[1m"+"\33[35m "+self.record[(i,p)]+": "+"\33[0m"+data+"\n"
					msgitem = MessageItem(sock, msg)
					#store user message into the message queue
					self.message_frame.put(msgitem)


			#abrupt user exit
			except:
				(i,p)=sock.getpeername()
				msg = "\r\33[31m \33[1m"+self.record[(i,p)]+" left the conversation unexpectedly\33[0m\n"
				msgitem = MessageItem(sock,data)
				self.message_frame.put(msgitem)
			
				print ("Client (%s, %s) is offline (error)" % (i,p)," [",self.record[(i,p)],"]\n")
				del self.record[(i,p)]
				self.connected_list.remove(sock)
				sock.close()
				connected = False
				continue
	#function to run the server 
	def run(self, host, port, client_Count):
        	#sys.exit()
		name=""
		self.client = int(client_Count)


		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind((host, port))
		server_socket.listen(10) #listen atmost 10 connection at one time

		# Add server socket to the list of readable connections
		self.connected_list.append(server_socket)

		print ("\33[32m \t\t\t\tSERVER WORKING \33[0m")
		clientcmd = 'gnome-terminal -- python3 client.py '+host+' '+ str(port);
		
		# Run the clints in Gnome terminal
		for _ in range(0,int(client_Count)):
			subprocess.call([clientcmd], shell=True)
		
		#Thread to send relay messages from a user to other users
		sendthread = threading.Thread(target=self.send_to_all, args=(server_socket,))
		sendthread.start()

		while 1:
		
			sockfd, addr = server_socket.accept()
			self.connected_list.append(sockfd)
			buffer = 4096

			name=sockfd.recv(buffer).decode("utf-8")
			
			self.record[addr]=""
			if name in self.record.values():
				sockfd.send("\r\33[31m\33[1m Username already taken!\n\33[0m")
				del self.record[addr]
				self.connected_list.remove(sockfd)
				sockfd.close()
				continue
			else:
		            	#add name and address
				self.record[addr]=name
				print ("Client (%s, %s) connected" % addr," [",self.record[addr],"]")
				sockfd.send("\33[32m\r\33[1m Welcome to chat room. Enter 'bye' anytime to exit\n\33[0m".encode())
				msg = "\33[32m\33[1m\r "+name+" joined the conversation \n\33[0m"		
				msgitem = MessageItem(sockfd,msg)
				self.message_frame.put(msgitem)
		
			#Threads to 
			thread = threading.Thread(target=self.handle_client, args=(sockfd, addr))
			self.threads.append(thread)
			thread.start()
			print (self.client)

			

		for t in self.threads:
	    		t.join()

		server_socket.close()


	


if __name__ == "__main__":
	if len(sys.argv)<2:
		host = "localhost"
		port = 5001
		client_Count = 2
	else:
		host = sys.argv[1]
		port = int(sys.argv[2])
		client_Count = sys.argv[3]
	Server().run(host, port, client_Count)
