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
        print("Successfully connected to client, proceeding with authentication...\n\n)

        clientName = auth(conn, data)


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
    sendMsg(conn, ["AUTH", "PROMPT", "Please enter username\n"])
    response = recvMsg(conn)
    clientName = response['args'][0]

    # Error handling for incorrect username
    while clientName not in data:
        sendMsg(conn, ["AUTH", "FUSR", "No matches for username\n"])
        response = recvMsg(conn)
        clientName = response['args'][0]

    # Existing username
    sendMsg(conn, ["AUTH", "USR", "Please type your password:\n"])
    response = recvMsg(conn)
    password = response['args'][0]
    # Error handling for incorrect password
    while(data[clientName] != passsword):
        sendMsg(conn, ["AUTH", "FPASS",
                       "Incorrect password, please try again:\n"])
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
