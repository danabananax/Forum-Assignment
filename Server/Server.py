from socket import *
import sys
import json
import os
# TODO
# Create data structure for forum
# Create entry message to user and work on first few operations


def start(port):
    # call function to retrieve data from file
    data = getData()
    # create socket and listen for 1 connection at a time
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', int(port)))
    serverSocket.listen(1)

    print("Listening for client request...\n\n")

    # Enter connection loop that initiates client interaction
    connect(serverSocket, data)


def getData():
    # parsing data fromd file into dictionary
    data = {}

    dir_path = os.path.dirname(os.path.realpath(__file__))
    credentials = os.path.join(dir_path, "credentials.txt")
    with open(credentials) as file:
        for line in file:
            user = line.split(" ")
            userName = user[0]
            userPass = user[1]
            data[userName] = userPass
    # return dictionary containing credential data
    return data

# WORK ON THIS


def connect(serverSocket, data):
    while True:
        try:
            # form connection to client, sending welcome message
            conn, addr = serverSocket.accept()
            print(
                "Successfully connected to client, proceeding with authentication...\n\n")

            clientName = auth(conn, data)
        except timeout():
            continue


def recvMsg(conn):
    data = conn.recv(1024).decode()
    message = json.loads(data)
    return message


def sendMsg(conn, message):
    code = message.pop(0)

    messageObj = {'code': code, 'args': message}
    data = json.dumps(messageObj).encode()
    conn.sendall(data)


def auth(conn, data):
    # First username prompt
    sendMsg(conn, ["AUTH", "PROMPT", "Please enter username:\n"])
    response = recvMsg(conn)
    clientName = response['args'][0]

    # Error handling for incorrect username
    while clientName not in data:
        sendMsg(conn, [
                "AUTH", "FUSR", "No matches for username, Please enter valid username:\n"])
        response = recvMsg(conn)
        clientName = response['args'][0]

    # Existing username
    sendMsg(conn, ["AUTH", "USR", "Please type your password:\n"])
    response = recvMsg(conn)
    password = response['args'][0]
    # Error handling for incorrect password
    while(data[clientName] != password):
        sendMsg(conn, ["AUTH", "FPASS",
                       "Incorrect password, please try again:\n"])
        response = recvMsg(conn)
        password = response['args'][0]

    # Presented username matches password, client is authenticated
    print("\nPassword correct.\n ")
    return clientName


# Take port as CL argument, if no port prompt user for number.
while True:
    try:
        PORT = sys.argv[1]
        break
    except IndexError:
        PORT = int(input("Port number not recognized, please enter port number"))
        break


start(PORT)
