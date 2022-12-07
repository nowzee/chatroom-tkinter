#import library
import socket
import threading
import rsa #bientot

host, port = '127.0.0.1',6666
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

clients = []
username = []

def boradcoast(namess):
    for client in clients:
        client.send(namess)

def send(client):
    while True:
        try:
            namess = client.recv(1024)
            boradcoast(namess)
            print(namess)
        except Exception:
            i = clients.index(client)
            clients.remove(client)
            client.close()
            name = username[i]
            boradcoast(f'{name} a quitté le groupe'.encode('utf-8'))
            username.remove(name)
            break

def receiveclient():
    while True:
        client, address = server.accept()
        print(f'client connecté avec {str(address)}')
        usernames = client.recv(1024).decode('utf-8')
        username.append(usernames)
        clients.append(client)
        boradcoast(f'{usernames} à rejoin le groupe'.encode('utf-8'))
        #log
        print(usernames)
        threading.Thread(target=send, args=(client,)).start()
receiveclient()
