#Server side code
import socket
from sys import exit

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_name = socket.gethostname()
server_ip = socket.gethostbyname(server_name)
print(f"\n========= I am Server ========\n")
print(f"Server Name: {server_name} IP: {server_ip}")

s.bind((server_ip,1025))
s.listen(5)
conn,ip = s.accept()

while True:
    data = conn.recv(4096)
    if not data:
        print("Disconnected....")
        break
    print(f"Data: {data.decode('utf-8')}")
    response = input("Your Mood: ")
    if response.lower() == "b":
        conn.sendall(b"The Server is going to Shut down")
        break
    else:
        conn.sendall(response.encode('utf-8'))

conn.close()
s.close()

