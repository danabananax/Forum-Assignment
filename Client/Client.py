# coding: utf-8
import socket
from socket import AF_INET, SOCK_STREAM
import json
import sys
from time import sleep
# Define connection (socket) parameters
# Address + Port no
# Server would be running on the same host as Client


def start():

    # connect to server
    while True:
        try:
            print("Creating socket...\n")
            # Take port as CL argument, if no port prompt user for number.
            while True:
                try:
                    PORT = int(sys.argv[1])
                    SERVER_IP = (sys.argv[2])
                    break
                except IndexError:
                    PORT = int(
                        input("Please reenter port number:\n"))
                    SERVER_IP = (input("Please reenter server IP:\n"))
                    print("\n\n")
                    break
            # create the socket
            clientSocket = socket.socket(AF_INET, SOCK_STREAM)
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

        session(clientSocket)
        continue


def clientAuth(socket):
    # receiving username prompt
    while True:
        response = recvText(socket)
        if(response['code'] == "AUTH" and response['args'][0] == "PASS"):
            print(response['args'][1])
            return True
        message = input(response['args'][1])
        sendText(socket, ["AUTH", message])


def recvText(socket):
    data = socket.recv(1024).decode()
    #print(f"decoded data: {data}\n\n")
    message = json.loads(data)
    return message


def sendText(socket, message):
    sleep(0.1)
    code = message.pop(0)
    messageObj = {'code': code, 'args': message}
    data = json.dumps(messageObj).encode()
    socket.sendall(data)


def session(socket):
    # default loop for standard client session
    while True:
        # presenting message from server as prompt
        response = recvText(socket)
        # print(f"response is {response}")
        # if subcode is start, client in session and needs input
        if response['args'][0] == "START":
            command = input(response['args'][1]).split(" ")
            # parsing input into list to send
            command[0] = command[0].upper()
            sendText(socket, command)
        # if client is not in session, just print message
        elif response['code'] == "XIT":
            break
        elif response['code'] == "UPD" and response['args'][0] == "RECV":
            upd(socket, response['args'][1])
        elif response['code'] == 'DWN' and response['args'][0] == "SEND":
            filename = response['args'][1]
            dwn(socket, filename)
        else:
            print(response['args'][1])
        continue

    print("\n\nThank you for visiting the forum!\n\n")
    sleep(3)
    socket.close()
    return


def upd(conn, filename):
    with open(filename, "rb") as f:
        packet = f.read(1024)
        while(packet):
            print("Sending\n")
            conn.sendall(packet)
            packet = f.read(1024)

    print("File sent\n")
    return


def dwn(conn, filename):
    # receive file
    content = b''
    conn.settimeout(3)
    while True:
        try:
            print("Receiving...\n")
            packet = conn.recv(1024)
            if not packet:
                break
            content += packet
        except socket.timeout:
            break

    with open(filename, "wb") as f:
        f.write(content)
    conn.settimeout(60)
    return


start()
