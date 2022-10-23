import socket
import threading

HOST = '127.0.0.1'
PORT = 1996
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
clients = []
names = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.pop(client)
            client.close()
            name = names[index]
            names.pop(name)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Conectado com: {address}")
        client.send('NICK'.encode('utf-8'))
        name = client.recv(1024)
        names.append(name)
        clients.append(client)
        broadcast(f'{name} se juntou ao chat!\n'.encode('utf-8'))
        client.send('Conectado ao servidor'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('Servidor executando!')
receive()