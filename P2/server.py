import socket
import sys
from thread import *
import time

'''
Function Definition
'''
def tupleToString(t):
	s=""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
HOST = ''	# Symbolic name meaning all available interfaces
PORT = 9486	# Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

'''
Bind socket to local host and port
'''
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket bind complete'

'''
Start listening on socket
'''
s.listen(10)
print 'Socket now listening'

# Start of the Skeleton Code

clients= []
userpass = [["user1", "passwd1"], ["user2", "passwd2"], ["user3", "passwd3"]]
messages = [[],[],[]]
subscriptions = [[],[],[]] # Store the group info

def clientthread(conn):
	global clients
	global count

	uppair = conn.recv(1024)
	uppair = stringToTuple(uppair)
	if uppair in userpass:
		user = userpass.index(uppair)
		conn.sendall('valid')
		print 'login successful'	
		'''
		Part-2:TODO: 
		After the user logs in, check the unread message for this user.
		Return the number of unread messages to this user.
		'''

		while True:
			try :
				option = conn.recv(1024)
			except:
				break
			if option == str(1):
				# Logout that you implemented in Part-1
				print 'User Logout'
				conn.close()
				if conn in clients:
					clients.remove(conn)

				break;
			elif option == str(2):
				message = conn.recv(1024)
				if message == str(1):
					'''
					Part-2:TODO: Send private message
					'''
					msgToSend = conn.recv(1024)
					rcv_id = conn.recv(1024)

				if message == str(2):
					'''
					Part-2:TODO: Send broadcast message
					'''
				if message == str(3):
					'''
					Part-2:TODO: Send group message
					'''
			elif option == str(3):
				'''
				Part-2:TODO: Join/Quit group
				'''
			elif option == str(4):
				'''
				Part-2:TODO: Read offline message
				'''
			else:
				try :
					conn.sendall('Option not valid')
				except socket.error:
					print 'option not valid Send failed'
					conn.close()
					clients.remove(conn)
	else:
		try :
			conn.sendall('nalid')
		except socket.error:
			print 'nalid Send failed'
	print 'Logged out'
	conn.close()
	if conn in clients:
		clients.remove(conn)

def receiveClients(s):
	# Use the code in Part-1, do some modification if necessary
	global clients
	while 1:
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		clients.append(conn)
		start_new_thread(clientthread, (conn,)) 

start_new_thread(receiveClients ,(s,))
while 1:
	message = raw_input()
	if message == 'messagecount':
		print 'Since the server was opened ' + str(count) + ' messages have been sent'
	elif message == 'usercount':
		print 'There are ' + str(len(clients)) + ' current users connected'
	elif message == 'storedcount':
		print 'There are ' + str(sum(len(m) for m in messages)) + ' unread messages by users'
	elif message == 'newuser':
		user = raw_input('User:\n')
		password = raw_input('Password:')
		userpass.append([user, password])
		messages.append([])
		subscriptions.append([])
		print 'User created'
	elif message == 'listgroup':
		'''
		Part-2:TODO: Implement the functionality to list all the available groups
		'''
s.close()
