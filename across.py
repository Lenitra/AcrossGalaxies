import random
import yaml
import datetime
import os

from cryptography.fernet import Fernet

secret_key = b'gZTtOPorjsy8tdTFeLWXKWqG9EcX1Ifd1oiaFDXgFFg='



def encode(message: str):
    key = secret_key
    message = bytes(message, "utf-8")
    return Fernet(key).encrypt(message)


def decode(token: bytes):
    key = secret_key
    return (Fernet(key).decrypt(token)).decode("utf-8")


def connect(mail, mdp):
    with open('data/accounts.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for users in data:
        if users["mail"] == mail and decode(users["mdp"]) == mdp:
            return users["pseudo"]
    return False


# Appelée pour register l'utilisateur
# Retourne :
# 0 si un champ est vide
# 1 si le mail est invalide
# 2 si le mail est déjà prit
# 3 si le pseudo est déjà prit
# 4 si le pseudo est pas conforme
# 5 si le mdp est pas conforme
# 255 enregistrement réussi !
def register(mail, mdp, pseudo):
    updateallplanets()
    plaid = 0
    while not checkpla(plaid):
        plaid = random.randint(0, 9999)


    with open('data/accounts.yaml') as f:
        users = yaml.load(f, Loader=yaml.FullLoader)

    if mail == "" or mdp == "" or pseudo == "":
        return 0

    if "@" in mail:
        if "." in mail.split("@")[1]:
            pass
        else:
            return 2
    else:
        return 2

    for e in users:
        if e["mail"] == mail:
            return 2

    for e in users:
        if e["pseudo"] == pseudo:
            return 3

    if len(mdp) <= 5:
        return 5

    else:
        mdp = encode(mdp)
        users.append({"mail": mail, "mdp": mdp, "pseudo": pseudo})

        with open('data/accounts.yaml', 'w') as f:
            data = yaml.dump(users, f)

        bat = {"puces": 1, "carbone": 1, "hydro": 1, "energy": 1,
               "lab": 0, "sp": 0}
        user = {"reco": datetime.datetime.now(), "vip": 0,
                plaid: {'bat': bat, 'ress': (100, 100, 100), 'lab': {},
                    'flotte': {}}}

        with open(f'data/players/{pseudo}.yaml', 'w') as f:
            data = yaml.dump(user, f)
        return 255

def getplanetslist(player):
    ress = {}
    with open(f'data/players/{player}.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for k, v in data.items():
        if k != "reco" and k != "vip":
            ress[k] = v["ress"]

    return ress

def checkpla(id):
    with open(f'data/planets.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    if data[id] != None:
        return False
    else:
        return True

def getpsd(mail):
    with open('data/accounts.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for user in data:
        if user["mail"] == mail:
            return user["pseudo"]

def updateallplanets():

    allpla = {}
    for e in range(10000):
        allpla[e] = None
    li = os.listdir("data/players")

    for e in li:
        with open(f'data/players/{e}') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        for d in data.keys():
            if d != "reco" and d != "vip":
                allpla[d] = e.split(".")[0]

    with open(f'data/planets.yaml', 'w') as f:
        data = yaml.dump(allpla, f)


def updateressource(player):
    onemore = False
    with open(f'data/players/{player}.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    delta = datetime.datetime.now() - data["reco"]
    delta = delta.total_seconds()
    delta = (delta/60)/60
    print(delta)
    if delta > 3:
        delta = 3
    for k,v in data.items():
        if k != "reco" and k != "vip":
            tmp1 = int(int(v["bat"]["carbone"])*10*(delta)) + v["ress"][0]
            tmp2 = int(int(v["bat"]["puces"]) * 10 * (delta)) + v["ress"][1]
            tmp3 = int(int(v["bat"]["hydro"]) * 10 * (delta)) + v["ress"][2]
            if tmp1 > v["ress"][0] or tmp2 > v["ress"][1] or tmp3 > v["ress"][2]:
                onemore = True
            data[k]["ress"] = (tmp1, tmp2, tmp3)

    if onemore:
        data["reco"] = datetime.datetime.now()
    with open(f'data/players/{player}.yaml', 'w') as f:
        data = yaml.dump(data, f)
    # Nb ress/h = lvl*10

def getbats(player, idpla):
    if idpla == "*":
        return {
            "carbone": ("*", "*", "*", "*"),
            "puces": ("*", "*", "*", "*"),
            "hydro": ("*", "*", "*", "*"),
            "lab": ("*", "*", "*", "*"),
            "sp": ("*", "*", "*", "*")
        }
    with open(f'data/players/{player}.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    c = (data[int(idpla)]["bat"]["carbone"],
         10 * data[int(idpla)]["bat"]["carbone"],
         5 * data[int(idpla)]["bat"]["carbone"],
         5 * data[int(idpla)]["bat"]["carbone"])

    p = (data[int(idpla)]["bat"]["puces"], 4 * data[int(idpla)]["bat"]["puces"],
         data[int(idpla)]["bat"]["puces"] * 9, data[int(idpla)]["bat"]["puces"]*7)

    h = (data[int(idpla)]["bat"]["hydro"],
         10 * data[int(idpla)]["bat"]["hydro"],
         8 * data[int(idpla)]["bat"]["hydro"],
         2 * data[int(idpla)]["bat"]["hydro"])

    lab = (data[int(idpla)]["bat"]["lab"], data[int(idpla)]["bat"]["lab"] * 4,
           data[int(idpla)]["bat"]["lab"] * 10, data[int(idpla)]["bat"]["lab"]*10)

    spaceport = (data[int(idpla)]["bat"]["sp"],
                 data[int(idpla)]["bat"]["sp"] * 10,
                 data[int(idpla)]["bat"]["sp"] * 10,
                 data[int(idpla)]["bat"]["sp"]*10)

    print(data[int(idpla)]["bat"])

    return {"carbone": c, "puces": p, "hydro": h, "lab": lab, "sp": spaceport}

def upbat(player, batim, couts, plaid):
    if plaid == "*":
        return 0
    with open(f'data/players/{player}.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    data[int(plaid)]["ress"] = (data[int(plaid)]["ress"][0] - couts[1],
                           data[int(plaid)]["ress"][1] - couts[2],
                           data[int(plaid)]["ress"][2] - couts[3])

    data[int(plaid)]["bat"][batim] += 1

    with open(f'data/players/{player}.yaml', 'w') as f:
        data = yaml.dump(data, f)


def getvaisposs(player, idpla):
    if idpla == "*":
        return '<h2>Veuillez améliorer votre spatioport pour pouvoir construire des vaisseaux</h3>'
    liste = ""
    with open(f'data/players/{player}.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    lvl = data[int(idpla)]["bat"]["sp"]

    if lvl < 1 :
        liste = "<h2>Veuillez améliorer votre spatioport pour pouvoir construire des vaisseaux</h3>"

    if lvl >= 1:
        liste += '''
          <section>
        <img src="../static/imgs/spaceship.png" alt="">
        <h4>Vaisseau 1</h4>
        <ul>
          <li>Construction</li>
          <li><img src="../static/imgs/carbon.png" alt="Carbone :"> 50</li>
          <li><img src="../static/imgs/cpu.png" alt="Puces :"> 50</li>
          <li><img src="../static/imgs/atome.png" alt="Hydrogène :"> 40</li>
          <li>
            <form action="/upbuild" method="POST" name="carbone">
              <input type="text" name="v1" value="">
              <button type="submit">
                Construire
              </button>
            </form>
          </li>
        </ul>
      </section>
    '''

    return liste