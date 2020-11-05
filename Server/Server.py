from socket import *
import sys
import json
# TODO
# Create data structure for forum
# Create entry message to user and work on first few operations


def start(port):
    # call function to retrieve data from file
    data = genData({})
    # create socket and listen for 1 connection at a time
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind('', port)
    serverSocket.listen(1)

    print("Listening for client request...\n\n")

    # Enter connection loop that initiates client interaction
    connect(serverSocket, data)


def genData(data):
    # parsing data fromd file into dictionary
    newData = data
    with open('credentials.txt') as file:
        for line in file:
            user = line.split(" ")
            userName = user[0]
            userPass = user[1]
            newData[userName] = userPass
    # return dictionary containing credential data
    return newData

# WORK ON THIS


def connect(serverSocket, data):
    while True:
        # form connection to client, sending welcome message
        conn, addr = serverSocket.accept()
        conn.sendall(b"AUTH\r\nConnected to the server!\r\n")

        clientName = auth(conn, data)


def recvMsg(conn):
    data = conn.recv(1024)
    message = json.loads(data)
    return message


def sendMsg(conn, *message):
    msgObj = {}
    for word in message:
        msgArgs.append(word)
    messageObj = {'code': message[0], 'args': msgArgs}
    data = json.dumps(message).encode()
    conn.sendall(data)


def auth(conn, data):
    # First username promprt
    sendMsg(conn, "AUTH", "PROMPT")
    clientName = recvMsg(conn)

    # Error handling for incorrect username
    while clientName[0] not in data:
        sendMsg(conn, "AUTH", "FUSR")
        clientName = recvMsg(conn)

    # Existing username
    sendMsg(conn, "AUTH", "USR")
    clientPass = recvMsg(conn)
    # Error handling for incorrect password
    while(data[clientName] != clientPass):
        sendMsg(conn, "AUTH", "Incorrect password, please try again: ")
        clientPass = recvMsg(conn)

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
