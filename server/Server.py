from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import ServerConstants as servconst
import Protocol
import random
import queue


ADDRESS = (servconst.HOST, servconst.PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

clients = {}
addresses = {}
inGame = {}
rooms = queue.Queue(maxsize=servconst.APP_BACKLOG)


# Set up handling for incoming clients
def accept():
    while True:
        (client, clientAddress) = SERVER.accept()
        print '>>>', clientAddress, 'has connected the server.'

        addresses[client] = clientAddress
        inGame[client] = False
        handlingThread = Thread(target=handleClient, args=(client,))
        handlingThread.start()


# Handle a single client connection
def handleClient(client):
    # for some reason the client needs to receive a first dummy message
    # in order to be capable of receiving the next messages
    client.send(bytes('<DUMMY IGNITION MESSAGE>'))

    while not inGame[client]:
        msg = client.recv(servconst.BUFFER_SIZE)
        print 'msg:', msg
        msg = Protocol.toDictionary(msg)

        if msg['type'] == servconst.GAME_SEARCH_MESSAGE:
            print '>>> Received request:', msg
            availableRoom = None

            if not rooms.full():
                # create new room
                if rooms.empty():
                    roomNum = random.randint(0, servconst.APP_BACKLOG)
                    gameElement = {'room_number': roomNum, 'participants': [client]}
                    rooms.put(gameElement)
                    permit = 0  # wait
                # join existing room
                else:
                    availableRoom = rooms.get()
                    roomNum = availableRoom['room_number']
                    availableRoom['participants'].append(client)
                    permit = 1  # allow
            else:
                permit = -1  # forbid
                roomNum = -1

            msg = {'type': servconst.GAME_SEARCH_MESSAGE, 'room': roomNum, 'permit': permit}
            if availableRoom is not None:
                print 'availableroom:', availableRoom['participants']
                for c in availableRoom['participants']:
                    print 'sending to', c, msg
                    c.send(bytes(msg))
            else:
                print 'single sending to', client, msg
                client.send(bytes(msg))


def removeRoom(chatServer):
    del rooms[chatServer.name]


SERVER.listen(servconst.APP_BACKLOG)
print '>>> Waiting for connection...'

ACCEPT_THREAD = Thread(target=accept)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
SERVER.close()
