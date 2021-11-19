from datetime import date, datetime, time
import mysql.connector
import os
import yaml
from confi import *

db = mysql.connector.connect(host=sql_host,
                             user=sql_user,
                             passwd=sql_password)

cursor = db.cursor()
now = datetime.now()
now = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"
# DB : AC
# Table : PInf

# Déplacement dans la DB
cursor.execute("USE AcrossGalaxies;")

print('START > PInf.sql')
cursor.execute("DROP TABLE PInf;")
cursor.execute(
    f"CREATE TABLE PInf(Psd varchar(255) NOT NULL, Reco DATETIME, Vip DATETIME, Staff INT, PRIMARY KEY (Psd));"
)
li = os.listdir("data/players")
for e in li:
    with open(f'data/players/{e}', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    pseudo = e.split(".")[0]
    reco = data["pinf"]["reco"]
    reco = f"{reco.year}-{reco.month}-{reco.day} {reco.hour}:{reco.minute}:{reco.second}"
    if pseudo != "Lenitra":
        cursor.execute(
            f'''INSERT INTO PInf VALUES ("{pseudo}", "{reco}", "{now}", 0);'''
        )
    else:
        cursor.execute(
            f'''INSERT INTO PInf VALUES ("{pseudo}", "{reco}", "{now}", 5);''')

print('END > PInf.sql')
print('START > Accounts.sql')

cursor.execute("DROP TABLE Accounts;")
cursor.execute(
    f"CREATE TABLE Accounts(Psd varchar(255) NOT NULL, Mail varchar(255) NOT NULL, Mdp varchar(255) NOT NULL, PRIMARY KEY (Psd));"
)

with open(f'data/accounts.yaml', encoding='utf8') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
for users in data:
    for k,v in users.items():
        if k == "mdp":
            mdp = v
        if k == "mail":
            mail = v
        if k == "pseudo":
            psd = v
    cursor.execute(
        f'''INSERT INTO Accounts VALUES ("{psd}", "{mail}", "{mdp}");''')

print('END > Accounts.sql')
print('START > Planets.sql')

cursor.execute("DROP TABLE Planets;")
print("création de la table incoming !")
cursor.execute(
    f"CREATE TABLE Planets(Plaid INT NOT NULL, Psd varchar(255), Shield DATETIME, Ress1 INT, Ress2 INT, Ress3 INT, carbone INT, hydro INT, puces INT, sp INT, rad INT, Croiseur INT, Nanosonde INT, Cargo INT, Victoire INT, Colonisateur INT, PRIMARY KEY (Plaid));"
)
allpla = {}
for e in range(1, 10000):
    allpla[e] = None
li = os.listdir("data/players")
for e in li:
    with open(f'data/players/{e}', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    pseudo = e.split(".")[0]
    for k,v in data.items():
        if k != "pinf":
            allpla[int(k)] = {}
            allpla[int(k)]["psd"] = pseudo
            allpla[int(k)]["ress"] = v["ress"]
            allpla[int(k)]["bat"] = v["bat"]
            allpla[int(k)]["shield"] = v["shield"]
            allpla[int(k)]["flotte"] = {}
            try:
                allpla[int(k)]["flotte"]["Croiseur"] = v["flotte"]["Croiseur"]
            except:
                allpla[int(k)]["flotte"]["Croiseur"] = 0

            try:
                allpla[int(k)]["flotte"]["Nano-Sonde"] = v["flotte"]["Nano-Sonde"]
            except:
                allpla[int(k)]["flotte"]["Nano-Sonde"] = 0

            try:
                allpla[int(k)]["flotte"]["Cargo"] = v["flotte"]["Cargo"]
            except:
                allpla[int(k)]["flotte"]["Cargo"] = 0

            try:
                allpla[int(k)]["flotte"]["Victoire"] = v["flotte"]["Victoire"]
            except:
                allpla[int(k)]["flotte"]["Victoire"] = 0

            try:
                allpla[int(k)]["flotte"]["Colonisateur"] = v["flotte"]["Colonisateur"]
            except:
                allpla[int(k)]["flotte"]["Colonisateur"] = 0


print(v["flotte"])
print('SAVE FINISH')

count = 1
for k,v in allpla.items():
    print(count)
    count += 1
    if v == None:
        cursor.execute(
            f'''INSERT INTO Planets VALUES ("{k}", NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);''')
    else:
        cursor.execute(
            f'''INSERT INTO Planets VALUES ("{k}","{v["psd"]}", "{v["shield"]}" ,{v["ress"][0]}, {v["ress"][1]}, {v["ress"][2]}, {v["bat"]["carbone"]}, {v["bat"]["puces"]}, {v["bat"]["hydro"]}, {v["bat"]["sp"]}, {v["bat"]["rad"]}, {v["flotte"]["Croiseur"]}, {v["flotte"]["Nano-Sonde"]}, {v["flotte"]["Cargo"]}, {v["flotte"]["Victoire"]}, {v["flotte"]["Colonisateur"]});'''
        )

print('END > Planets.sql')

# start = datetime.now()
# cursor.execute("SELECT Ress1 FROM Planets WHERE Plaid='9999';")

# recup = cursor.fetchall()

# print(recup[0][0])
# print(datetime.now() - start)

db.commit()

db.close()
