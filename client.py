import socket, select, string, sys
import time


class Client(object):
	# function to print messages in terminal
	def display(self) :
		you="\33[33m\33[1m"+" You: "+"\33[0m"
		sys.stdout.write(you)
		sys.stdout.flush()
		
		
	def run(self, host, port):

		#asks for user name
		name=input("\33[34m\33[1m CREATING NEW ID:\n Enter username: \33[0m")
		print(name)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(20)
	    
	    	# connecting host
		try:
			s.connect((host, port))
		except :
			print ("\33[31m\33[1m Can't connect to the server \33[0m")
			time.sleep(60)
			#sys.exit()

		#if connected
		s.send(name.encode())
		self.display()
		while 1:
			socket_list = [sys.stdin, s]

			# Get the list of sockets which are readable
			rList, wList, error_list = select.select(socket_list , [], [])

			for sock in rList:
			    #incoming message from server
				if sock == s:
					data = sock.recv(4096)
					data = data.decode("utf-8")
				
					if not data :
					    continue
					    print ('\33[31m\33[1m \rDISCONNECTED!!\n \33[0m')
					    #sys.exit()
					else :
					    sys.stdout.write(data)
					    self.display()

			    #user entered a message
				else :
					msg=sys.stdin.readline().encode()
					s.send(msg)
					self.display()
					if msg == "bye".encode():
						sys.exit()	


if __name__ == "__main__":
	if len(sys.argv)<2:
		host = "localhost"
		port = 5001
	else:
		host = sys.argv[1]
		port = sys.argv[2]
	Client().run(host, int(port))
	
    	
    
