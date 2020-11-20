import socket
from socket import AF_INET, SOCK_STREAM
import sys
import json
import os
from time import sleep
# TODO
# create threadExists() and getLines()
# finish and test msg()


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
    with open(credentials, "r") as file:
        for line in file:
            user = line.split(" ")
            userName = user[0]
            userPass = user[1]
            data[userName] = userPass
    # return dictionary containing credential data
    return data


def connect(serverSocket, data):
    while True:
        try:
            # form connection to client, sending welcome message
            conn, addr = serverSocket.accept()
            print(
                "Successfully connected to client, proceeding with authentication...\n\n")

            clientName = auth(conn, data)
            print("Launching session...\n\n")
            session(conn, clientName)
        except socket.error as e:
            print(f"{e}\n\nConnecting to new client...\n\n")
            continue


def session(conn, username):
    # session input loop
    while True:
        message = ["AUTH", "START",
                   "\n\n\nPlease enter one of the following commands:\n\nCRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT, SHT\n\n"]
        sendMsg(conn, message)

        response = recvMsg(conn)
        # print(f"\n\nresponse is {response}\n\n")
        code = response['code'].upper()
        arguments = response['args']
        if code == "CRT":
            crt(conn, username, arguments)
            continue
        elif code == "MSG":
            msg(conn, username, arguments)
        elif code == "DLT":
            dlt(conn, username, arguments)
            continue
        elif code == "EDT":
            edt(conn, username, arguments)
            continue
        elif code == "LST":
            lst(conn)
            continue
        elif code == "RDT":
            rdt(conn, username, arguments)
            continue
        elif code == "UPD":
            upd(conn, username, arguments)
            continue
        elif code == "DWN":
            dwn(conn, username, arguments)
            continue
        elif code == "RMV":
            rmv(conn, username, arguments)
            continue
        elif code == "XIT":
            xit(conn, username, arguments)
            continue
        elif code == "SHT":
            sht(conn, username, arguments)
            continue
        else:
            message = ["AUTH", "SESSION", "Please enter valid code\n\n"]
            sendMsg(conn, message)
            continue


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
    sendMsg(conn, ["AUTH", "PASS",
                   "\nAuthentication successful, welcome to the forum\n\n"])
    print("\nPassword correct.\n ")
    return clientName


def crt(conn, username, response):
    # Setting up list of current files in cwd
    print(f"name of file to be created {response}\n")
    # checking through files list
    try:
        threadtitle = response[0]
    except IndexError:
        errorMsg = "Number of arguments does not match number of needed arguments, try again\n"
        sendMsg(conn, [
                "AUTH", "ERR", errorMsg])
        return

    # if thread exists, send err
    filename = f"{threadtitle}.txt"
    if os.path.exists(filename):
        message = f"forum \"{threadtitle}\" exists. Try again\n\n"
        response = ["AUTH", "ERR", message]
        sendMsg(conn, response)
        return

    with open(filename, "w") as f:
        f.write(f"{username}\n")
    print(f"Successfully created file \"{filename}\"\n\n")
    response = ["AUTH", "SUCCESS",
                f"Success! {threadtitle} has been created.\n\n"]
    sendMsg(conn, response)
    return


def dlt(conn, username, arguments):
    threadtitle = arguments[0]
    messageNumber = arguments[1]
    # checking if threadtitle exists
    if not checkThread(conn, threadtitle):
        return
    # create list defining every line before editing
    filename = f"{threadtitle}.txt"
    with open(filename, "r") as f:
        lines = f.readlines()
    # checking if message number is valid
    if not validMsgNum(conn, lines, messageNumber):
        return
    # check if username == author of msg
    if not isAuthor(conn, username, lines, messageNumber):
        return
    # write to new file, ignoring deleted line
    with open(filename, "w") as f:
        newLines = []
        for line in lines:
            if " " not in line:
                newLines.append(line)
                continue
            msgSplit = line.split(" ")
            msgNum = msgSplit[0]
            msgUsr = msgSplit[1]
            # removing colon from username from file
            msgUsr = msgUsr[:-1]
            # skip message to delete from being written to new file
            if msgNum == messageNumber and msgUsr == username:
                continue
            # write all other lines to 'new' file
            newLines.append(line)
        f.writelines(newLines)

    # create object representing new lines to reset msg numbers
    with open(filename, "r") as f:
        lines = f.readlines()
    # write updated line messages to new file
    with open(filename, "w") as f:
        newLines = []
        newMsgNum = 1
        for line in lines:
            # skipping author line #1
            if " " not in line:
                newLines.append(line)
                continue
            # split and change msg number and write to new file
            # msgSplit = [msgNumber, author, message\n]
            msgSplit = line.split(" ")
            msgSplit[0] = str(newMsgNum)
            newMsgNum += 1
            newLine = " ".join(msgSplit)

            newLines.append(newLine)

        f.writelines(newLines)
    print(
        f"Successfully deleted message number {messageNumber} from {filename}\n")
    sendMsg(conn, ["AUTH", "SUCCESS",
                   f"Message {messageNumber} has been successfully deleted from {threadtitle}.\n"])
    return


def isAuthor(conn, username, lines, messageNumber):
    for line in lines:
        # skipping first author line
        if " " not in line:
            continue
        # checking if user == author of message
        msgSplit = line.split(" ")
        currMsgNum = msgSplit[0]
        currUsername = msgSplit[1]
        currUsername = currUsername[:-1]
        print(f"currUsername = {currUsername}, username = {username}\n")
        if currMsgNum == messageNumber and currUsername != username:
            message = [
                "AUTH", "ERR", f"You are not the author of message number {messageNumber}. Try again\n"]
            sendMsg(conn, message)
            return False
    print("User is author of message\n")
    return True


def validMsgNum(conn, lines, messageNumber):
    try:
        if int(messageNumber) < 1 or int(messageNumber) > len(lines) + 1:
            message = "message number exceeds number of messages. Try again\n\n"
            sendMsg(conn, ["AUTH", "ERR", message])
            return False
    # if msg number isnt numeric raise err
    except ValueError:
        message = "Input for message number is not numeric, please try again\n\n"
        sendMsg(conn, ["AUTH", "ERR", message])
        return False
    print("Message number is valid\n")
    return True


def msg(conn, username, arguments):
    # parse arguments
    try:
        threadtitle = arguments[0]
        msgContent = arguments[1]
    except IndexError:
        errorMsg = "Number of arguments does not match number of needed arguments, try again\n"
        sendMsg(conn, [
                "AUTH", "ERR", errorMsg])
        return
    # if thread does not exist
    if not checkThread(conn, threadtitle):
        return

    filename = f"{threadtitle}.txt"
    with open(filename, "r") as f:
        lines = f.readlines()
    # msgNum is len(lines) because messages start on line 2
    msgNum = len(lines)
    with open(filename, "a") as f:
        f.write(f"{msgNum} {username}: {msgContent}\n")

    sendMsg(conn, ["AUTH", "SUCCESS", "Message sent.\n"])
    print(f"Message {msgContent} written by {username} to {filename}\n")
    return


def edt(conn, username, arguments):
    try:
        # parse arguments
        threadtitle = arguments[0]
        messageNumber = arguments[1]
        newMessage = arguments[2]
    # error handling for wrong number of arguments
    except IndexError:
        errorMsg = "Number of arguments does not match number of needed arguments, try again\n"
        sendMsg(conn, [
                "AUTH", "ERR", errorMsg])
        return
    # check if threadtitle exists
    if not checkThread(conn, threadtitle):
        return
    # Check for authoritative request (username == author of msg)
    filename = f"{threadtitle}.txt"
    with open(filename, "r") as f:
        lines = f.readlines()

    # if msg number is too high, send err
    if not validMsgNum(conn, lines, messageNumber):
        return

    # if user isnt author, send err
    if not isAuthor(conn, username, lines, messageNumber):
        return

    # edit corresponding message with new msg
    newLines = []
    with open(filename, "w") as f:
        for line in lines:
            if " " not in line:
                newLines.append(line)
                continue
            msgSplit = line.split(" ")
            print(f"msg split up is {msgSplit}\n")
            currMsgNum = msgSplit[0]
            currUsername = msgSplit[1]
            currUsername = currUsername[:-1]
            # change corresponding msg to new msg + \n
            if(currMsgNum == messageNumber and currUsername == username):
                msgSplit[2] = f"{newMessage}\n"
            newLine = " ".join(msgSplit)
            newLines.append(newLine)
        f.writelines(newLines)

    print(
        f"Successfully edited message {messageNumber} to \"{newMessage}\" in {threadtitle}\n")
    message = "Message successfully edited.\n"
    sendMsg(conn, ["AUTH", "SUCCESS", message])
    return


def lst(conn):
    # get all files in current directory
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    # if no threads to display send err
    if len(files) <= 1:
        message = "There are no threads to display, create thread before trying again\n"
        sendMsg(conn, ["AUTH", "ERR", message])
        return
    # display all files
    threadList = []
    for file in files:
        if file == "credentials.txt" or file[-2:] == 'py':
            continue
        threadList.append(file)
    lst_string = "\n".join(threadList)
    sendMsg(conn, ["LST", "SUCCESS", lst_string])
    return


def recvMsg(conn):
    data = conn.recv(1024).decode()
    message = json.loads(data)
    return message


def sendMsg(conn, message):
    sleep(0.1)
    code = message.pop(0)
    messageObj = {'code': code, 'args': message}
    data = json.dumps(messageObj).encode()
    conn.sendall(data)
# return false if thread does not exist, true otherwise


def checkThread(conn, threadtitle):
    filename = f"{threadtitle}.txt"
    if not os.path.exists(filename):
        message = f"Thread {threadtitle} does not exist in forum, try again\n"
        sendMsg(conn, ["AUTH", "ERR", message])
        return False
    print("Check thread passed\n")
    return True


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
