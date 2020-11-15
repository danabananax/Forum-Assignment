import socket
from socket import AF_INET, SOCK_STREAM
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
    serverSocket = socket.socket(AF_INET, SOCK_STREAM)
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
            session(conn, clientName)
        except socket.error as e:
            print(f"{e}\n\nConnecting to new client...\n\n")
            continue


def session(conn, username):
    # Sending welcome message and starting input loop for commands

    # session input loop
    while True:
        message = ["AUTH", "START",
                   "\nPlease enter one of the following commands:\n\nCRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT, SHT\n\n"]
        sendMsg(conn, message)

        response = recvMsg(conn)
        code = response.pop(0)

        if code == "CRT":
            crt(conn, username, response)
            continue
        elif code == "DLT":
            dlt(conn, username, response)
            continue
        elif code == "EDT":
            edt(conn, username, response)
            continue
        elif code == "LST":
            lst(conn, username, response)
            continue
        elif code == "RDT":
            rdt(conn, username, response)
            continue
        elif code == "UPD":
            upd(conn, username, response)
            continue
        elif code == "DWN":
            dwn(conn, username, response)
            continue
        elif code == "RMV":
            rmv(conn, username, response)
            continue
        elif code == "XIT":
            xit(conn, username, response)
            continue
        elif code == "SHT":
            sht(conn, username, response)
            continue
        else:
            message = ["AUTH", "SESSION", "Please enter valid code\n\n"]
            sendMsg(conn, message)
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


def crt(conn, username, response):
    # Setting up list of current files in cwd
    cwd = os.getcwd()
    files = [f for f in os.listdir(
        cwd) if os.path.isfile(os.path.join(cwd, f))]
    # checking through files list
    threadtitle = response[0]
    filename = f"{threadtitle}.txt"

    if filename not in files:
        message = f"forum \"{threadtitle}\" does not exist. Try again\n\n"
        response = ["AUTH", "ERR", message]
        sendMsg(conn, response)
        return
    else:
        f = open(filename, "w+")
        f.write(f"{username}\n")
        f.close()

        response = ["AUTH", "SUCCESS",
                    f"Success! {threadtitle} has been created.\n\n"]
        return


# Take port as CL argument, if no port prompt user for number.
while True:
    try:
        PORT = sys.argv[1]
        adminPass = sys.argv[2]
        break
    except IndexError:
        PORT = int(input("Port number not recognized, please enter port number"))
        break


start(PORT)
