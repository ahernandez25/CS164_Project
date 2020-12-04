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

onlineUsers = []
clients= []
userpass = [["user1", "passwd1"], ["user2", "passwd2"], ["user3", "passwd3"]]
userIndex = ["user1", "user2", "user3"] 
messages = [[],[],[]]
subscriptions = [[],[],[]] # Store the group info

def clientthread(conn):
	global clients
	global count

	uppair = conn.recv(1024)
	uppair = stringToTuple(uppair)
	if uppair in userpass:
		user = userpass.index(uppair)
		clients.append(conn)
		onlineUsers.append(user)
		print "user " + str(user) + "logged in\n"
		conn.sendall('valid')
		print 'login successful'	

		'''
		Part-2:TODO: 
		After the user logs in, check the unread message for this user.
		Return the number of unread messages to this user.
		'''

		if messages[user] : 
			numMsgs = len(messages[user])
			conn.sendall(str(numMsgs))
		else :
			conn.sendall(str(0))

		while True:
			
			print "Number users: " + str(len(onlineUsers))
			
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
				onlineUsers.remove(user)
				break;
			elif option == str(2):
				message = conn.recv(1024)
				if message == str(1):
					'''
					Part-2:TODO: Send private message
					'''
					msgToSend = conn.recv(1024)
					rcv_id = conn.recv(1024)
				
					if rcv_id in userIndex : 
						rcvIndex = userIndex.index(rcv_id)
						messages[rcvIndex].append(msgToSend)
						msg = "Message sent"
					else : 
						 msg = "User not found. Select another user"

					conn.sendall(msg) 
	

				if message == str(2):
					'''
					Part-2:TODO: Send broadcast message
					'''
					bmsg = conn.recv(1024)

					
					for u in onlineUsers : 
						if u != user :
							if u == 0 :
								print "\nuser 1 online"
								messages[0].append(bmsg)
							elif u == 1 : 
								print "\nuser2 online"
								messages[1].append(bmsg)
							else : 
								print "\nuser3 online"
								messages[2].append(bmsg)
						else : 
							print "current user\n"

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
				print "Read offline messages\n"
				option = conn.recv(1024)
				print "recieved option\n"
				if option == str(1) : 
					print "in option 1\n"
					

					if messages[user] :
						print "have messages to read"
						message = "messages to read" 
						conn.sendall(message)
						messages[user].clear()
					else : 
						print "In else- no new messages"
						message = "No offline messages"
						conn.sendall(message)
						print "message sent"
				elif option == str(2) : 
					conn.sendall(str(2))	
				else : 
					conn.sendall("Option not valid")
					conn.close()
					if conn in clients :
						clients.remove(conn)
					if user in onlineUsers :
						onlineUsers.remove(user)
			else:
				try :
					conn.sendall('Option not valid')
				except socket.error:
					print 'option not valid Send failed'
					conn.close()
					if user in onlineUsers :
						onlineUsers.remove(user)
					if conn in clients: 
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
	if user in onlineUsers : 
		onlineUsers.remove(user)
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
