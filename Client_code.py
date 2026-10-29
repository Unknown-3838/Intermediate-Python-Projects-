import socket
from sys import exit

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
name = socket.gethostname()
server_ip = socket.gethostbyname(name)
# server_ip = "127.0.0.1"

print(f"\n========= I am Client =========\n")
try:
    s.connect((server_ip,1025))
    print("Connected...")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

while True:
    try:
        send_d = input("What You want to send: ")
        s.send(send_d.encode('utf-8'))

        data = s.recv(4096)
        if not data:
            print("Server Band")
            break
        print(f"Data Received: {data.decode('utf-8')}")
        
    except Exception as e:
        print("Error: ",e)
        break
s.close()

