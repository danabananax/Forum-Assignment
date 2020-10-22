#coding: utf-8
from socket import *

# Define connection (socket) parameters
# Address + Port no
# Server would be running on the same host as Client
serverName = 'localhost'


def start():
    print("Creating socket...\n")
    # Take port as CL argument, if no port prompt user for number.
    while True:
        try:
            PORT = sys.argv[1]
            break
        except IndexError:
            PORT = int(
                input("Port number not recognized, please enter port number"))
            break
    # create the socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # connect to server
    while True:
        try:
            # estalish TCP conmnection
            clientSocket.connect(('localhost', PORT))
        except clientSocket.timeout:
            print("Connection timed out, trying again...")


clientSocket.send(sentence)
# As the connection has already been established, the client program simply drops the bytes in the string sentence into the TCP connection. Note the difference between UDP sendto() and TCP send() calls. In TCP we do not need to attach the destination address to the packet, as was the case with UDP sockets.

modifiedSentence = clientSocket.recv(1024)
# We wait to receive the reply from the server, store it in modifiedSentence

print 'From Server:', modifiedSentence
# print what we have received

clientSocket.close()
# and close the socket
