from datetime import date, datetime, time
import mysql.connector
import os
import yaml
from confi import *
from reqsql import *



def getbackup():
    now = datetime.now()
    datet = now
    now = f"{now.year}-{now.month}-{now.day}"
    os.mkdir(f"../backup/{now}")

    with open(f'../backup/{now}/Planets.yaml', 'w', encoding='utf8') as f:
        yaml.dump(retbrut("SELECT * FROM Planets WHERE Psd != 'None'"),f)

    with open(f'../backup/{now}/PInf.yaml', 'w', encoding='utf8') as f:
        yaml.dump(retbrut("SELECT * FROM PInf"),f)

    with open(f'../backup/{now}/Accounts.yaml', 'w', encoding='utf8') as f:
        yaml.dump(retbrut("SELECT * FROM Accounts"),f)

    # print(datetime.now() - datet)


def pushbackup(date):
    now = datetime.now()
    # region Backup PLANETS

    with open(f'../backup/{date}/Planets.yaml', 'r', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)


    a = retbrut("SELECT Plaid FROM Planets WHERE Psd != 'None'")
    if len(a) > 0:
        for e in a:
            print(f"Suppression du plaid : {e[0]}")
            reqsql(
                f"UPDATE Planets SET Psd = NULL, Shield = NULL, Ress1 = NULL, Ress2 = NULL, Ress3 = NULL, carbone = NULL, hydro = NULL, puces = NULL, sp = NULL, rad = NULL, Croiseur = NULL, Nanosonde = NULL, Cargo = NULL, Victoire = NULL, Colonisateur = NULL WHERE Plaid = {e[0]};"
            )



    for pla in data:
        print(f"Push plaid : {pla[0]}")
        reqsql(
            f"UPDATE Planets SET Psd = '{pla[1]}', Shield = '{pla[2]}', Ress1 = {pla[3]}, Ress2 = {pla[4]}, Ress3 = {pla[5]}, carbone = {pla[6]}, hydro = {pla[7]}, puces = {pla[8]}, sp = {pla[9]}, rad = {pla[10]}, Croiseur = {pla[11]}, Nanosonde = {pla[12]}, Cargo = {pla[13]}, Victoire = {pla[14]}, Colonisateur = {pla[15]} WHERE Plaid = {pla[0]};"
        )
    # endregion


    # region Backup PInf

    with open(f'../backup/{date}/PInf.yaml', 'r', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    print("Suppression des datas des joueurs")
    reqsql("TRUNCATE TABLE PInf")

    for player in data:
        print(f"Push player : {player[0]}")
        reqsql(f"INSERT INTO PInf VALUES('{player[0]}', '{player[1]}', '{player[2]}', {player[3]})")
    # endregion


    # region Backup Accounts

    with open(f'../backup/{date}/Accounts.yaml', 'r', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    print("Suppression des datas des joueurs")
    reqsql("TRUNCATE TABLE Accounts")

    for player in data:
        print(f"Push Account de : {player[0]}")
        player = (f'"{player[0]}"', f'"{player[1]}"', f'"{player[2]}"')
        reqsql(
            f"INSERT INTO Accounts VALUES({player[0]}, {player[1]}, {player[2]})"
        )
    # endregion

    print(datetime.now() - now)




# getbackup()
# pushbackup("2021-12-11")