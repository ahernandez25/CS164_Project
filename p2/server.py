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
groupNames = ["Group 1", "Group 2", "Group 3"]
groupMsg = [[],[],[]]

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

					#conn.sendall(msg) 
	

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
					gmsg = conn.recv(1024)
					print(gmsg)
					
					g_id = conn.recv(10)
					print(g_id)
					if g_id in groupNames :
						i = groupNames.index(g_id)		
						groupMsg[i].append(gmsg)
						print groupMsg[i]
					else :
						print "group doesnt exist\n"


			elif option == str(3):
				'''
				Part-2:TODO: Join/Quit group
				'''
				option = conn.recv(1024)
				print option + "\n"
				if option == str(1) :
					joinGroup = conn.recv(25)		
					print joinGroup + "\n"
					if joinGroup in groupNames :
						i = groupNames.index(joinGroup)
						subscriptions[i].append(user)
						print "User : " + str(subscriptions[i]) + " joined " + groupNames[i]				
					else : 
						print "Group name invalid"
		
				elif option == str(2) :
					quitGroup = conn.recv(20)
					if quitGroup in groupNames :
                                                i = groupNames.index(quitGroup)
                                                subscriptions[i].remove(user)
                                                print "User : " + str(user)  + " quit " + groupNames[i]	

				elif option == str(3) :
					groups = ""

                        	        for g in groupNames :
                        			print g + "\n"
						groups = groups + " " + g
						

                        		print(groups)
                        		conn.sendall(groups)
				else : 
					print("Invalid option")
		
			elif option == str(4):
				'''
				Part-2:TODO: Read offline message
				'''
				option = conn.recv(1024)
				if option == str(1) : 

					if messages[user] :
						print "have messages to read"
						msg = ""
						for x in  messages[user] : 
							msg = msg + x + "\n"
						
						print(msg)
						conn.sendall(msg)
						messages.pop(user)
					else : 
						print "In else- no new messages"
						message = "No offline messages"
						conn.sendall(message)
				elif option == str(2) : 
					g_id = conn.recv(20)
					print(g_id)
					if g_id in groupNames :
						i = groupNames.index(g_id)
						msg = ""
						for x in groupMsg[i] :
							msg = msg + x + "\n"
						print(msg)
						conn.sendall(msg)
	
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
