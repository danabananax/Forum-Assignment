from socket import *
import sys
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


def recvText(conn):
    response = conn.recv(1024).decode()
    responseParse = response.split("\r\n\r\n")
    message = responseParse[0]
    return message


def sendText(conn, msg):
    message = msg + "/r/n/r/n"
    message = message.encode()
    conn.sendall(message)


def auth(conn, data):
    # First username promprt
    sendText(conn, "Please enter username: ")
    clientName = recvText(conn)

    # Error handling for incorrect username
    while clientName not in data:
        sendText(conn, "Username does not exist, please type valid username:")
        clientName = recvText(conn)

    # Error handling for incorrect password
    sendText(conn, "Please enter the password for this account: ")
    clientPass = recvText(conn)
    while(data[clientName] != clientPass):
        sendText(conn, "Incorrect password, please try again: ")
        clientPass = recvText(conn)

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
