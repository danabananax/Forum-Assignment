# coding: utf-8
import socket
from socket import AF_INET, SOCK_STREAM
import json
import sys
# Define connection (socket) parameters
# Address + Port no
# Server would be running on the same host as Client


def start():
    print("Creating socket...\n")
    # Take port as CL argument, if no port prompt user for number.
    while True:
        try:
            PORT = int(sys.argv[1])
            SERVER_IP = int(sys.argv[2])
            break
        except IndexError:
            PORT = int(
                input("Please reenter port number:\n"))
            SERVER_IP = int(input("Please reenter server IP:\n"))
            print("\n\n")
            continue
    # create the socket
    clientSocket = socket.socket(AF_INET, SOCK_STREAM)

    # connect to server
    while True:
        try:
            # estalish TCP conmnection
            clientSocket.connect((SERVER_IP, PORT))
            print("Success! Establishing connection\n\n")
        except socket.error as e:
            print(f"{e}\n\n")
            continue

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
    while True:
        response = recvText(socket)
        if(response['code'] == "AUTH" and response['args'][0] == "PASS"):
            break
        message = input(response['args'][1])
        sendText(socket, ["AUTH", message])


def recvText(conn):
    data = conn.recv(1024).decode()
    message = json.loads(data)
    return message


def sendText(conn, message):

    code = message.pop(0)
    messageObj = {'code': code, 'args': message}
    data = json.dumps(messageObj).encode()
    conn.sendall(data)


start()
