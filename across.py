import random
from re import M
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
               "lab": 1, "sp": 1}
        user = {"pinf":{"reco": datetime.datetime.now(), "vip": 0},
                plaid: {'bat': bat, 'ress': (100, 100, 100), 'lab': {},
                    'flotte': {}}}

        with open(f'data/players/{pseudo}.yaml', 'w') as f:
            data = yaml.dump(user, f)
        return 255

def getplanetslist(player):
    ress = {}
    plalist=''
    with open(f'data/players/{player}.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for k, v in data.items():
        if k != "pinf":
            v = v["ress"]

            plalist +=f'''
                <li>
                <form action="/updatedata" method="POST" name="{k}">
                <input type="text" name="pla" value ="{k}" class="hide">
                <button type="submit">
                <h3>Planète #{k}</h3>
                <p>C : {v[0]} | P : {v[1]} | H : {v[2]}</p>
                </button>
                </form>
                </li>
                '''
    return plalist

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

# Permet l'update de "/data/planets.yaml"
def updateallplanets():

    allpla = {}
    for e in range(10000):
        allpla[e] = None
    li = os.listdir("data/players")

    for e in li:
        with open(f'data/players/{e}') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        for d in data.keys():
            if d != "pinf":
                allpla[d] = e.split(".")[0]

    with open(f'data/planets.yaml', 'w') as f:
        data = yaml.dump(allpla, f)

# Système de récolte des ressources
def updateressource(player):
    onemore = False
    with open(f'data/players/{player}.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    delta = datetime.datetime.now() - data["pinf"]["reco"]
    delta = delta.total_seconds()
    delta = (delta/60)/60
    if delta > 3:
        delta = 3
    for k,v in data.items():
        if k != "pinf":
            tmp1 = int(int(v["bat"]["carbone"])*10*(delta)) + v["ress"][0]
            tmp2 = int(int(v["bat"]["puces"]) * 10 * (delta)) + v["ress"][1]
            tmp3 = int(int(v["bat"]["hydro"]) * 10 * (delta)) + v["ress"][2]
            if tmp1 > v["ress"][0] or tmp2 > v["ress"][1] or tmp3 > v["ress"][2]:
                onemore = True
            data[k]["ress"] = (tmp1, tmp2, tmp3)

    if onemore:
        data["pinf"]["reco"] = datetime.datetime.now()
    with open(f'data/players/{player}.yaml', 'w') as f:
        data = yaml.dump(data, f)
    # Nb ress/h = lvl*10

# Retourne les couts d'amélioration d'un batiment en fonction de son lvl (c,p,h)
def getcostup(bat, lvl):
    cost = 0
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    cost = (data["Infra"][bat])
    for _ in range(lvl-1):
        cost[0] += cost[0]/2
        cost[1] += cost[1]/2
        cost[2] += cost[2]/2
    cost[0] = int(cost[0])
    cost[1] = int(cost[1])
    cost[2] = int(cost[2])
    return cost

# Retourne un dictionnaire contenant les couts d'upgrade des batiments
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
    tmp = getcostup("Carbone", data[int(idpla)]["bat"]["carbone"])
    c = (data[int(idpla)]["bat"]["carbone"],
         tmp[0],
         tmp[1],
         tmp[2])

    tmp = getcostup("Puces", data[int(idpla)]["bat"]["puces"])
    p = (data[int(idpla)]["bat"]["puces"], tmp[0], tmp[1], tmp[2])

    tmp = getcostup("Hydro", data[int(idpla)]["bat"]["puces"])
    h = (data[int(idpla)]["bat"]["hydro"], tmp[0], tmp[1], tmp[2])

    tmp = getcostup("Lab", data[int(idpla)]["bat"]["lab"])
    lab = (data[int(idpla)]["bat"]["lab"], tmp[0], tmp[1], tmp[2])

    tmp = getcostup("Sp", data[int(idpla)]["bat"]["sp"])
    spaceport = (data[int(idpla)]["bat"]["sp"], tmp[0], tmp[1], tmp[2])


    return {"carbone": c, "puces": p, "hydro": h, "lab": lab, "sp": spaceport}

# Améliora un batiment et retire les ressources du joueur
def upbat(player, batim, couts, plaid):
    if plaid == "*":
        return 0
    addplayerress(player, plaid, (-couts[1],-couts[2],-couts[3]))
    with open(f'data/players/{player}.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)


    data[int(plaid)]["bat"][batim] += 1

    with open(f'data/players/{player}.yaml', 'w') as f:
        data = yaml.dump(data, f)

# Récupère le html des vaisseaux dispo en fonction du lvl du sp
def getsp(player, idpla):
    if idpla == "*":
        return '<h2>Veuillez améliorer votre spatioport pour pouvoir construire des vaisseaux</h3>'
    liste = ""
    with open(f'data/players/{player}.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    lvl = data[int(idpla)]["bat"]["sp"]

    with open(f'config.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    if lvl < 1:
        liste = "<h2>Veuillez améliorer votre spatioport pour pouvoir construire des vaisseaux</h3>"

    for k,v in data["Vaisseaux"].items():
        if v[3] <= lvl:
            liste += f'''
        <style>
            #{k} {{
                background-image: url("../static/imgs/{k}.png");
                background-repeat: no-repeat;
                background-size: 20%;
             }}
        </style>
        <section id="{k}">
        <h4>{k}</h4>
        <ul>
          <li>Construction</li>
          <li><img src="../static/imgs/carbon.png" alt="Carbone :"> {v[0]}</li>
          <li><img src="../static/imgs/cpu.png" alt="Puces :"> {v[1]}</li>
          <li><img src="../static/imgs/atome.png" alt="Hydrogène :"> {v[2]}</li>
          <li>
            <form action="/upship" method="POST" name="vinf">
              <input type="text" name="vinf" value="{k}" class="hide">
              <input type="text" name="nb" value="">
              <button type="submit">
                Construire
              </button>
            </form>
          </li>
        </ul>
      </section>
    '''
    return liste

# Ajoute un vaisseau et retourne la liste de vaisseaux construits
def addvaisseau(player, plaid, vaiss, nb):
    with open(f'data/players/{player}.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    if vaiss != None:
        try:
            data[int(plaid)]["flotte"][vaiss] = int(nb)+int(data[int(plaid)]["flotte"][vaiss])
        except:
            data[int(plaid)]["flotte"][vaiss] = int(nb)
    re = data[int(plaid)]["flotte"]
    with open(f'data/players/{player}.yaml', 'w') as f:
        data = yaml.dump(data, f)
    return re

# Retourne le html des vaisseaux construitss
def gethang(player, idpla):
    if idpla == "*":
        return '<h2>Aucun vaisseau sur cette planette</h3>'
    liste = ""
    flotte = addvaisseau(player, idpla, None, None)

    if flotte == {} :
        liste = '<h2>Aucun vaisseau sur cette planette</h3>'
    for k, v in flotte.items():
        liste += f'''
            <style>
            #{k} {{
                background-image: url("../static/imgs/{k}.png");
                background-repeat: no-repeat;
                background-size: 20%;
             }}
        </style>
          <section id="{k}">
            <h4>{k} - ({v})</h4>
          </section>
        '''
    
    return liste

# Modifie les ressources du jouer et les retournes
def addplayerress(player, plaid, ress):
    if plaid == "*":
        return ("*", "*", "*")
    with open(f'data/players/{player}.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    data[int(plaid)]["ress"] = (data[int(plaid)]["ress"][0]+ress[0], data[int(plaid)]["ress"][1]+ress[1], data[int(plaid)]["ress"][2]+ress[2])
    re = data[int(plaid)]["ress"]
    with open(f'data/players/{player}.yaml', 'w') as f:
        data = yaml.dump(data, f)

    return re

# Récupère le cout de création d'un "nb" de vaisseaux
def getvaisscost(vaiss, nb):
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    cost = data["Vaisseaux"][vaiss]
    cost[0] = -cost[0]*int(nb)
    cost[1] = -cost[1]*int(nb)
    cost[2] = -cost[2]*int(nb)
    return cost