# This File handles the FTP Project for the summer Agile class at PSU 2017


# Imports
import ftplib as ft
# State vars
ftp_connection = None
connection_name = None


# Connects to the
def connect(host, username="", password="", account_info=""):
    global ftp_connection
    ftp_connection = ft.FTP(host, username, password, account_info)
    print("Connected")


def help_menu():
    print("Options : \n"
          "Quit \n"
          "Connect <host username password> \n"
          "Close \n")


def parse_input():
    u_input = input("input: ")
    u_input = u_input.split()
    if u_input[0] == "Quit":
        return True
    elif u_input[0] == "Connect":
        if len(u_input) == 4:
                connect(u_input[1], u_input[2], u_input[3])
        else:
            connect(u_input[1])
    elif u_input[0] == "Close":
        if ftp_connection is not None:
            ftp_connection.close()
        else:
            print("No Connection to Close")
    return False


if __name__ == "__main__":
    done = False
    while not done:
        help_menu()
        done = parse_input()
