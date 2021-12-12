from datetime import datetime, timedelta
import json
from typing import Container
from werkzeug.wrappers.request import PlainRequest
import yaml
from random import randint

from reqsql import readsql, reqsql, retbrut

def contain(liste, element):
    for e in liste:
        if e == element:
            return True
    return False


oldinscrits = readsql("SELECT COUNT(*) FROM Accounts")[0]
nbpla = readsql("SELECT COUNT(*) FROM Planets")[0]
if (oldinscrits*20 <= nbpla):
    # Créer 20 planètes vierges
    for i in range(20):
        nbpla +=1
        reqsql(f"INSERT INTO Planets(Plaid) VALUES({nbpla})")
    

#     pla = (
#         newplaid[tamp],
#         data[tamp][1],
#         data[tamp][2],
#         data[tamp][3],
#         data[tamp][4],
#         data[tamp][5],
#         data[tamp][6],
#         data[tamp][7],
#         data[tamp][8],
#         data[tamp][9],
#         data[tamp][10],
#         data[tamp][11],
#         data[tamp][12],
#         data[tamp][13],
#         data[tamp][14],
#         data[tamp][15]
#     )

# oldplaid = []

# with open('backup/2021-12-11/Planets.yaml', encoding='utf8') as f:
#     data = yaml.load(f, Loader=yaml.FullLoader)
# for e in data:
#     oldplaid.append(e[0])

# newplaid = []

# print(oldplaid)

# tmp = oldplaid.copy()

# count = 0

# for e in tmp:

#     print(e)
#     if e < 360:
#         oldplaid.remove(e)
#         newplaid.append(e)
#         count += 1
# print(count)

# for e in oldplaid:
#     rand = randint(10, 360)
#     while contain(newplaid, rand):
#         rand = randint(10, 360)
#     newplaid.append(rand)

# # print(oldplaid)
# # newplaid.sort()
# print(newplaid)

# planets = []

# toret = []

# tamp = 0

# for e in data:
#     pla = (
#         newplaid[tamp],
#         data[tamp][1],
#         data[tamp][2],
#         data[tamp][3],
#         data[tamp][4],
#         data[tamp][5],
#         data[tamp][6],
#         data[tamp][7],
#         data[tamp][8],
#         data[tamp][9],
#         data[tamp][10],
#         data[tamp][11],
#         data[tamp][12],
#         data[tamp][13],
#         data[tamp][14],
#         data[tamp][15]
#     )
#     planets.append(pla)

#     tamp += 1

# with open(f'newbackup.yaml', 'w', encoding='utf8') as f:
#     data = yaml.dump(planets, f)

# reqsql("""
# CREATE TABLE Planets (
#     Plaid        INTEGER PRIMARY KEY,
#     Psd          VARCHAR(255),
#     Shield       DATETIME,
#     Ress1        INTEGER,
#     Ress2        INTEGER,
#     Ress3        INTEGER,
#     carbone      INTEGER,
#     hydro        INTEGER,
#     puces        INTEGER,
#     sp           INTEGER,
#     rad          INTEGER,
#     Croiseur     INTEGER,
#     Nanosonde    INTEGER,
#     Cargo        INTEGER,
#     Victoire     INTEGER,
#     Colonisateur INTEGER
#     )""")

# with open('data/stats.yaml', encoding='utf8') as f:
#     data = yaml.load(f, Loader=yaml.FullLoader)

# data["homeunique"] = {}

# with open(f'data/stats.yaml','w',encoding='utf8') as f:
#         data = yaml.dump(data, f)

# titre = "Version B45"
# desc = "Changelog du 15/12/2021"
# changes = []
# changes.append("Nouvelle home page")
# changes.append("Lors d'une selection de vaisseaux en destination d'un autre planète, vous pourrez voir la taille, puissance et le stockage de votre selection")
# changes.append("Popup de confirmation lorsqu'il manque des ressources pour une construction")
# changes.append("Système de backups")
# changes.append("Système de maintenance qui bloque l'accès au jeu")
# changes.append("(bug visuel) Fix des stats des vaisseaux dans l'interface spacioport")
# changes.append("(Invisible) Panel admin avec logs")
# changes.append("Modification mineures")

# addchangelog(titre, desc, changes)

# METTRE TOUT LES JOUEURS VIP

# players = retbrut("SELECT Psd FROM PInf")
# for player in players:
#     player= player[0]
#     reqsql(
#         f'''
#         UPDATE PInf SET Vip = '{datetime.now()+timedelta(days= 1000)}' WHERE Psd = '{player}';
#     '''
#     )
