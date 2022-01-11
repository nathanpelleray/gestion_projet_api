from fastapi import FastAPI
import threading
import time
import socket


"""
VARIABLES EN COMMUN
"""
threadsClients = []
info = []

"""
GESTION DES RASPBERRY
"""

def envoiMessage(client, nom):
    client.send(nom.encode("utf-8"))


def demandeInfo(client, info):
    if info[0] == "tmp":
        client.send(info[0].encode("utf-8"))
        info[0] = client.recv(255)
        info[0].decode("utf-8")
    

def serveur():
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind(('', 5575))
    serveur.listen(5)

    while True:
        client, infosClient = serveur.accept()
        threadsClients.append((client, infosClient))

    serveur.close()


socketServeur = threading.Thread(None, serveur, None, (), {})
socketServeur.start()



"""
GESTION DES CLIENTS
"""

app = FastAPI()

@app.get("/")
async def root():
    return {"root"}


@app.get("/{ip}/infotemp")
async def root(ip):
    global info
    for i in range(len(threadsClients)):
        if threadsClients[i][1][0] == ip:
            client = threadsClients[i][0]
            info[0] = "tmp"
            thread = threading.Thread(None, demandeInfo, None, (client, info), {})
            thread.start()
            thread.join()
        
    return {info[0]}


@app.get("/{ip}/{nom}")
async def test(ip, nom):
    for i in range(len(threadsClients)):
        if threadsClients[i][1][0] == ip:
            client = threadsClients[i][0]
            thread = threading.Thread(None, envoiMessage, None, (client, nom), {}) 
            thread.start()
        
    return {"OK"}