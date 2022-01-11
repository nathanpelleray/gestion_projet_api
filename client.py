import socket
adresseIP = "127.0.0.1"	# Ici, le poste local
port = 5575	# Se connecter sur le port 50000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((adresseIP, port))

while True:
    reponse = client.recv(255)
    print(reponse.decode("utf-8"))

    client.send("10".encode("utf-8"))

client.close()