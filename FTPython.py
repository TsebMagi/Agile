# This File handles the FTP Project for the summer Agile class at PSU :w17


# Imports
import ftplib as ft
import os
import sqlite3
import base64
from Crypto.Cipher.XOR import new

# State vars
ftp_connection = None
connection_name = None
total_bytes_transferred = 0

# Constants
DB_Name = "connections.db"

create_table = """CREATE TABLE IF NOT EXISTS connections (connection_name text PRIMARY KEY, connection_address text NOT NULL,
 port integer, user_name text, encrypted_password text); """
insert_into_table = """insert into connections values (?, ?, ?, ?, ?)"""
get_connections = """SELECT * from connections"""


# Changes a file's permissions, where change is the chmod xxxx fileName
def change_permissions(change):
    success_or_fail = ftp_connection.sendCommand(change)
    if success_or_fail is False:
        print("Failed to change permissions.")
    else:
        print("Successfully changed permissions.")


# Deletes a filename specified by the user
def delete(filename):
    try:
        ftp_connection.delete(filename)
        print("Successfully able to delete ", filename)
    except ft.all_errors as err:
        print("Unable to delete file " + filename + ": ", err)


# Connects to the host and updates the global ftp connection.
def connect(host, port=20, username="", password="", account_info=""):
    print("Trying to connect with user: ", username)
    print("Trying to connect with host: ", host)
    print("Trying to connect with port: ", port)
    print("Trying to connect with password: ", password)
    global ftp_connection
    try:
        ftp_connection = ft.FTP()
        print(ftp_connection.connect(host, port))
        print(ftp_connection.login(username, password, account_info))
        print(ftp_connection.pwd())
    except ft.all_errors as err:
        print("Connection failed: ", err)


# Places file(s) on the connected server
def put(files):
    global total_bytes_transferred
    for file in files:
        total_bytes_transferred = 0
        ftp_connection.storbinary("STOR " + os.path.basename(file), open(file, 'r+b'),
                                  8192, g_print_progress(file, os.path.getsize(file)))
        print("")


# Change directory (currently this is a relative path)
def cd(path):
    ftp_connection.cwd(path)


# List files in current directory
# Will not list . and .. - restriction of os.listdir command
def list_files(option):
    if option == "local":
        # print(os.listdir())
        for i in os.listdir():
            print(i)
        print('\n')
    elif option == "remote":
        if ftp_connection is not None:
            ftp_connection.dir()
        else:
            print("No Connection")
    else:
        print("Entered an Invalid option")


# Gets file(s) from the connected server
def get(files):
    global total_bytes_transferred
    for file in files:
        total_bytes_transferred = 0
        store_file = open(os.path.basename(file), 'w+b')
        ftp_connection.retrbinary("RETR " + file,
                                  g_write_and_print_progress(store_file, file, ftp_connection.size(file)))
        print("")
        store_file.close()


# Generates and returns the function to write the transferred bytes to
# a file and print the progress of the file transfer.
# This generation is necessary to use the returned function as the callback function for the
# get command, since the callback function is only allowed to take a single argument.
def g_write_and_print_progress(store_file, filename, file_size):
    def write_and_print_progress(bytes_transferred):
        store_file.write(bytes_transferred)
        print_function = g_print_progress(filename, file_size)
        print_function(bytes_transferred)

    return write_and_print_progress


# Generates and returns the function to calculate and print the progress of a file transfer.
# The print formatting was found on https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
# This generates the callback function for the put command.
#
# Note: This bugs in Pycharm as the lines don't always overwrite each other properly.  This
# is an issue with Pycharm.  If you run this in a normal terminal, it works fine.
def g_print_progress(filename, file_size):
    def print_progress(bytes_transferred):
        global total_bytes_transferred
        total_bytes_transferred = total_bytes_transferred + len(bytes_transferred)
        percent_done = float(total_bytes_transferred) / float(file_size)
        print("\r{1}    [{0:10s}] {2:.1f}%".format('#' * int(percent_done * 10), filename, percent_done * 100),
              end="", flush=True)

    return print_progress


def rename(option, old, new):
    try:
        if option == "local":
            os.rename(old, new)
        elif option == "remote":
            ftp_connection.rename(old, new)
    except FileNotFoundError:
        print("Rename: Invalid input")


# Prints the Basic Menu
def help_menu():
    print("Options : \n"
          "connect <host [port] username password> \n"
          "put <filename filename ...>\n"
          "get <filename filename ...>\n"
          "cd <path>\n"
          "rename <local/remote fromFilename toFilename>\n"
          "delete <filename> \n"
          "list remote \n"
          "list local \n"
          "save connection\n"
          "show connections\n"
          "close \n"
          "quit \n"
          "help \n"
          "change <chmod xxx file_name \n")


# Creates the Database if one doesn't exist yet and makes a basic table
def db_create():
    db_connection = sqlite3.connect(DB_Name)
    if db_connection is not None:
        db_connection.execute(create_table)
    else:
        print("Unable to connect to Database!")


# Prompts the user for the info to save the ftp connection in the local database
# will encrypt the password before storing it.
def save_connection():
    handle = input("Nickname: ")
    host = input("Hostname: ")
    port = input("Port (optional): ")
    username = input("Username(optional): ")
    password = input("Password(optional): ")
    key = input("Database Key (required if password is supplied): ")
    encode = None
    if len(password) > 0:
        if len(key) > 0:
            cypher = new(key)
            encode = cypher.encrypt(password)
        else:
            print("Error: Missing Key for password encryption Try again")
            return
    try:
        con = sqlite3.connect(DB_Name)
        c = con.cursor()
        c.execute(insert_into_table, (handle, host, port, username, encode))
        con.commit()
        con.close()
    except sqlite3.Error as err:
        print(err)


def show_connections():
    con = sqlite3.connect(DB_Name)
    c = con.cursor()
    c.execute(get_connections)
    output = c.fetchall()
    for item in output:
        print(item)


# Parses user input
def parse_input():
    u_input = input("input: ")
    u_input = u_input.split()
    u_input[0] = u_input[0].lower()

    try:
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
                del u_input[0]
                put(u_input)

        elif u_input[0] == "get":
            if len(u_input) < 2:
                print("You need to supply a file to download")
            else:
                del u_input[0]
                get(u_input)

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
            if len(u_input) >= 2:
                list_files(u_input[1])
            else:
                print("List requires an argument of 'local' or 'remote'.")

        elif u_input[0] == "help":
            help_menu()

        elif u_input[0] == "save":
            save_connection()

        elif u_input[0] == "show":
            show_connections()

        elif u_input[0] == "delete":
            delete(u_input[1])

        elif u_input[0] == "change":
            if u_input[1] is None or u_input[2] is None or u_input[3] is None:
                print("Error. Must provide permissions and file name.")
            else:
                change_permissions(u_input[1] + " " +
                               u_input[2] + " " + u_input[3])
        else:
            print("Invalid command.  Type help to display a help menu")
    except ft.all_errors as err:
        print("Error: ", err)
    return False


if __name__ == "__main__":
    done = False
    db_create()
    print("Welcome to our basic FTP client.\nType help to display a help menu\n")
    while not done:
        done = parse_input()
