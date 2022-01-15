from fastapi import FastAPI
import threading
import time
import socket
from request import *


"""
VARIABLES EN COMMUN
"""
info_Raspberry = {}
raspberry = None

"""
GESTION DES RASPBERRY
"""

"""
FONCTION UTILE
"""

def envoiMessage(client, message):
    client.send(message.encode("utf-8"))


def processRequest(request):
    data = request.dict()
    
    # Switch 1 (RED)
    if data["switch1"] == "on":
        envoiMessage(raspberry, "1:1")
    else:
        envoiMessage(raspberry, "1:0")

    time.sleep(0.08)

    # Switch 2 (GREEN)
    if data["switch2"] == "on":
        envoiMessage(raspberry, "2:1")
    else:
        envoiMessage(raspberry, "2:0")

    time.sleep(0.08)

    # Switch 3 (BLUE)
    if data["switch3"] == "on":
        envoiMessage(raspberry, "3:1")
    else:
        envoiMessage(raspberry, "3:0")

    time.sleep(0.08)

    # Range 1
    envoiMessage(raspberry, f"04:{data['range1']}")
    time.sleep(0.08)

    # Range 2
    envoiMessage(raspberry, f"05:{data['range2']}")
    time.sleep(0.08)

    # Range 3
    envoiMessage(raspberry, f"06:{data['range3']}")
    time.sleep(0.08)

    # Range 4
    envoiMessage(raspberry, f"10:{data['range4']}")


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

        message_content = message.split(":")
        info_Raspberry[message_content[0]] = message_content[1]
        
        print("{message} is processed...")

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
        # print("raspberry's server don't running !")
        time.sleep(2)

print("Connected to raspberry !")


"""
FONCTION DE L'API
"""

app = FastAPI()

# Requête pour information des capteurs
@app.get("/infos")
async def infos():
    print(info_Raspberry)
    return {"temperature": info_Raspberry['07'], "distance": info_Raspberry['09'], "humidite": info_Raspberry['08']}


# Requête à communiquer au raspeberry
@app.post("/")
async def request(request: Request):
    processRequest(request)
    return {"message": "La requête à bien été effectuée.."}