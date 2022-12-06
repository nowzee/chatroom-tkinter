#import library
import socket
import threading
import rsa #bientot

host, port = '127.0.0.1',6666
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

clients = []

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
            boradcoast(f'Une personne a quitté le groupe'.encode('utf-8'))
            break

def receiveclient():
    while True:
        client, address = server.accept()
        print(f'client connecté avec {str(address)}')
        names = client.recv(1024).decode('utf-8')
        boradcoast(f'une personne à rejoin le groupe'.encode('utf-8'))
        clients.append(client)
        #log
        print(names)
        threading.Thread(target=send, args=(client,)).start()

receiveclient()