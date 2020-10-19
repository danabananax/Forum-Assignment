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
    serverSocket.bind('localhost', port)
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
        conn, addr = serverSocket.accept()
        print("Connected with server!\n\n")

        clientName = auth(data)


def auth(data):
    clientName = input("Please enter username: ")
    try:
        while clientName not in data:
            clientName = input(
                "Username does not exist, please type valid username: ")

        clientPass = input("Please enter the password for this account: ")
        while(data[clientName] != clientPass):
            clientPass = input("Incorrect password, please try again: ")
    finally:
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
