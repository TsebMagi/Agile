# This File handles the FTP Project for the summer Agile class at PSU 2017


# Imports
import ftplib as ft
import os

# State vars
ftp_connection = None
connection_name = None
total_bytes_transferred = 0


# Connects to the host and updates the global ftp connection.
def connect(host, port=20, username="", password="", account_info=""):
    global ftp_connection
    try:
        ftp_connection = ft.FTP()
        print(ftp_connection.connect(host, port))
        print(ftp_connection.login(username, password, account_info))
    except ft.all_errors as err:
        print("Could not connect: ", err)


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
def g_print_progress(filename, file_size):
    def print_progress(bytes_transferred):
        global total_bytes_transferred
        total_bytes_transferred = total_bytes_transferred + len(bytes_transferred)
        percent_done = float(total_bytes_transferred) / float(file_size)
        print("\r{1}    [{0:10s}] {2:.1f}%".format('#' * int(percent_done * 10), filename, percent_done * 100),
              end="", flush=True)

    return print_progress


# Prints the Basic Menu
def help_menu():
    print("Options : \n"
          "connect <host [port] username password> \n"
          "put <filename filename ...>\n"
          "get <filename filename ...>\n"
          "cd <path>\n"
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
