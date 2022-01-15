from fastapi import FastAPI
import threading
import time
import socket
from request import *


"""
VARIABLES EN COMMUN
"""
info = {}
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
        print(f"switch1 : {data['switch1']}")
        envoiMessage(raspberry, "1:0")

    time.sleep(0.08)

    # Switch 2 (GREEN)
    if data["switch2"] == "on":
        print(f"switch2 : {data['switch2']}")
        envoiMessage(raspberry, "2:1")
    else:
        envoiMessage(raspberry, "2:0")

    time.sleep(0.08)

    # Switch 3 (BLUE)
    if data["switch3"] == "on":
        envoiMessage(raspberry, "3:1")
    else:
        print(f"switch3 : {data['switch3']}")
        envoiMessage(raspberry, "3:0")

    time.sleep(0.08)

    # Range 1
    envoiMessage(raspberry, f"04:{data['range1']}")
    print(f"04:{data['range1']}")
    time.sleep(1)

    # Range 2
    envoiMessage(raspberry, f"05:{data['range2']}")
    print(f"05:{data['range2']}")
    time.sleep(0.1)

    # Range 3
    envoiMessage(raspberry, f"06:{data['range3']}")
    print(f"06:{data['range3']}")
    time.sleep(0.1)

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

        # info[type(message_content[0])] = message_content[1]
        # if message_content[0] == "09":
        #     info["09"] = message_content[1]
        # elif message_content[0] == "07":
        #     info["07"] = message_content[1]  
            
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

@app.get("/infos")
async def infos():
    pass


@app.post("/")
async def request(request: Request):
    processRequest(request)
    return request

"""
FONCTION DE TEST
"""

@app.get("/")
async def root():
    return {"root"}


@app.get("/test")
async def test():
    envoiMessage(raspberry, "01:00")


@app.get("/info")
async def info():
    message = "09 : " + str(info["09"])
    return {message}

