# This File handles the FTP Project for the summer Agile class at PSU 2017


# Imports
import ftplib as ft
# State vars
ftp_connection = None
connection_name = None


# Connects to the host and updates the global ftp connection.
def connect(host, username="", password="", account_info=""):
    global ftp_connection
    ftp_connection = ft.FTP(host, username, password, account_info)
    print("Connected")


# Prints the Basic Menu
def help_menu():
    print("Options : \n"
          "Connect <host username password> \n"
          "List \n"
          "Close \n"
          "Quit \n" )


# Parses user input
def parse_input():
    u_input = input("input: ")
    u_input = u_input.split()
    u_input[0].lower()

    if u_input[0] == "quit":
        return True

    elif u_input[0] == "connect":
        if len(u_input) == 4:
                connect(u_input[1], u_input[2], u_input[3])
        else:
            connect(u_input[1])

    elif u_input[0] == "close":
        if ftp_connection is not None:
            ftp_connection.close()
        else:
            print("No Connection to Close")

    elif u_input[0] == "list":
        if ftp_connection is not None:
            ftp_connection.nlst('LIST')
        else:
            print("No Connection")
    return False


if __name__ == "__main__":
    done = False
    while not done:
        help_menu()
        done = parse_input()
