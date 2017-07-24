# This File handles the FTP Project for the summer Agile class at PSU 2017


# Imports
import ftplib as ft
import os
# State vars
ftp_connection = None
connection_name = None


# Connects to the host and updates the global ftp connection.
def connect(host, port=20, username="", password="", account_info=""):
    global ftp_connection
    try:
        ftp_connection = ft.FTP()
        print(ftp_connection.connect(host, port))
        print(ftp_connection.login(username, password, account_info))
    except ft.all_errors as err:
        print("Could not connect: ", err)


# Places a file on the connected server
def put(file):
    ftp_connection.storlines("STOR " + os.path.basename(file), open(file, 'r+b'))


# Change directory (currently this is a relative path)
def cd(path):
    ftp_connection.cwd(path)


# Get a file from the connected server
def get(file):
    ftp_connection.retrlines("RETR " + file, open(file, 'w').write)

def rename(option, old, new):
    try:
        if option == "local":
            os.rename(old, new)
        elif option == "remote":
            ftp_connection.rename(old, new)
    except(FileNotFoundError):
        print("Rename: Invalid input")


# Prints the Basic Menu
def help_menu():
    print("Options : \n"
          "connect <host [port] username password> \n"
          "put <filename>\n"
          "get <filename>\n"
          "cd <path>\n"
          "rename <local/remote fromFilename toFilename>\n"
          "list \n"
          "close \n"
          "quit \n"
          "help \n")


# Parses user input
def parse_input():
    u_input = input("input: ")
    u_input = u_input.split()
    u_input[0] = u_input[0].lower()

    if u_input[0] == "quit":
        return True

    elif u_input[0] == "connect":
        if len(u_input) == 4:
            connect(u_input[1], 20, u_input[2], u_input[3])
        elif len(u_input) == 5:
            connect(u_input[1], int(u_input[2]), u_input[3], u_input[4])
        else:
            connect(u_input[1])

    elif u_input[0] == "put":
        if len(u_input) < 2:
            print("You need to supply a filename to upload")
        else:
            put(u_input[1])

    elif u_input[0] == "get":
        if len(u_input) < 2:
            print("You need to supply a file to download")
        else:
            get(u_input[1])

    elif u_input[0] == "cd":
        if len(u_input) < 2:
            print("You need to supply a directory to go to")
        else:
            cd(u_input[1])

    elif u_input[0] == "rename":
        rename(u_input[1], u_input[2], u_input[3])

    elif u_input[0] == "close":
        if ftp_connection is not None:
            ftp_connection.close()
        else:
            print("No Connection to Close")

    elif u_input[0] == "list":
        if ftp_connection is not None:
            ftp_connection.dir()
        else:
            print("No Connection")

    elif u_input[0] == "help":
        help_menu()


    else:
        print("Invalid command.  Type help to display a help menu")
    return False


if __name__ == "__main__":
    done = False
    print("Welcome to our basic FTP client.\nType help to display a help menu\n")
    while not done:
        done = parse_input()
