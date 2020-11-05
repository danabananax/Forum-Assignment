#coding: utf-8
from socket import *
import json
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
            continue
    # create the socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # connect to server
    while True:
        try:
            # estalish TCP conmnection
            clientSocket.connect(('localhost', PORT))
        except clientSocket.timeout:
            print("Connection timed out, trying again...")

        # Error handling authentication
        while True:
            if(not clientAuth(clientSocket)):
                print("Authentication not successful, trying again...\n")
                continue
            else:
                break

 # WHERE WE LEFT OFF


def clientAuth(socket):
    # receiving username prompt
    response = recvText(socket)

    if(usernamePrompt == "Please enter username: "):
        # error handling for non-existant username
        while True:
            # send username after recieving prompt
            userName = input(usernamePrompt)
            sendText(socket, userName)

            response = recvText(socket)
            if(response == "Please enter the password for this account: "):
                break
            else:
                print(f"Username ")


def recvText(conn):
    response = conn.recv(1024).decode()
    responseParse = response.split("\r\n\r\n")
    message = responseParse[0]
    return message


def sendText(conn, msg):
    message = msg + "/r/n/r/n"
    message = message.encode()
    conn.sendall(message)
