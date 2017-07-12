import ftplib as ft

ftp_connection = None
connection_name = None


def connect(connection, host, username="", password="", account_info=""):
    connection = ft.FTP(host, username, password, account_info)
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
        connect(ftp_connection, u_input[1], u_input[2], u_input[3])
    elif u_input[0] == "Close":
        return True
    return False

if __name__ == "__main__":
    done = False
    while not done:
        help_menu()
        done = parse_input()
