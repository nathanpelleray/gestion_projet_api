from fastapi import FastAPI
import threading
import time
import socket


"""
VARIABLES EN COMMUN
"""
client = None

"""
GESTION DES RASPBERRY
"""

"""
FONCTION UTILE
"""

def envoiMessage(client, message):
    client.send(message.encode("utf-8"))



"""
RECEPTION DES DONNÉES DU RESPBERRY
"""

def serveur():
    print("Starting server ...")
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind(('', 5575))
    serveur.listen(5)

    client, infosClient = serveur.accept()
    print("New incoming connection...")

    while True:
        message = client.recv(255)
        message = message.decode("utf-8")
        print(message)

    serveur.close()

# Création du serveur où le raspberry se connecte
socketServeur = threading.Thread(None, serveur, None, (), {})
socketServeur.start()



"""
ENVOIE DES DONNÉES AU RESPBERRY
"""

raspberryIP = "192.168.1.82"	# Ici, le poste local
raspberryPort = 5575	# Se connecter sur le port 50000

print("Trying to connect to {raspberryIP}:{raspberryPort} ...")

flag = True
raspberry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while flag:
    try:
        raspberry.connect((raspberryIP, raspberryPort))
        flag = False
    except:
        print("raspberry's server don't running !")
        time.sleep(2)

print("Connected to raspberry !")


"""
GESTION DES CLIENTS
"""

app = FastAPI()

@app.get("/")
async def root():
    return {"root"}


@app.get("/test")
async def test():
    envoiMessage(raspberry, "01:00")
