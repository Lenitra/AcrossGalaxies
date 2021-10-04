from email.mime import text
import string

from confi import *
import random
import yaml
import datetime
import os
import platform
import smtplib
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart





def encode(message: str):
    key = secret_key
    message = bytes(message, "utf-8")
    return Fernet(key).encrypt(message)


def decode(token: bytes):
    key = secret_key
    return (Fernet(key).decrypt(token)).decode("utf-8")


def connect(mail, mdp):
    with open('data/accounts.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for users in data:
        if users["mail"] == mail and decode(users["mdp"]) == mdp:

            addlog(f"{getpsd(mail)} s'est connecté")

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
    plaid = 1
    while checkpla(plaid) != False:
        plaid = random.randint(1, 9999)


    with open('data/accounts.yaml', encoding='utf8') as f:
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

        bat = {"puces": 1, "carbone": 1, "hydro": 1,
               "rad": 1, "sp": 1}
        user = {
            "pinf": {
                "reco": datetime.datetime.now(),
                "vip": 0,
                "msgs": {}
            },
            plaid: {
                'bat': bat,
                'ress': (250, 250, 250),
                'flotte': {},
                "shield": datetime.datetime.now()
            }
        }
        with open(f'data/players/{pseudo}.yaml', 'w', encoding='utf8') as f:
            data = yaml.dump(user, f)
        addlog(f"{pseudo} s'est inscrit avec le mail {mail}")
        addshield(pseudo, plaid, 48)
        sendmsg(pseudo, ("Bienvenue !", "Bienvenue sur le jeu Across Galaxies ! Si vous avez des question je vous prie de rejoindre le serveur discord. En vous souhaitant un bon jeu ! Cordialement l'équipe de Across-Galaxies"))
        return 255


def addshield(player, plaid, hours):

    shield = 0

    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    if data[int(plaid)]["shield"] <= datetime.datetime.now():

        myDate = datetime.datetime.now()
        td = datetime.timedelta(hours = hours)
        shield = myDate + td

        data[int(plaid)]["shield"] = shield
        with open(f'data/players/{player}.yaml', 'w', encoding='utf8') as f:
            data = yaml.dump(data, f)
    else:
        shield = data[int(plaid)]["shield"]
    return shield

def delshield(player, plaid):
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    shield = datetime.datetime.now()
    data[int(plaid)]["shield"] = shield
    with open(f'data/players/{player}.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(data, f)


def getplanetslist(player):
    ress = {}
    plalist=''
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
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
                <p>C : {v[0]}<br>P : {v[1]}<br>H : {v[2]}</p>
                </button>
                </form>
                </li>
                '''
    return plalist

# Check si une planète est occupée et si oui retourne le psd du joueur
def checkpla(id):
    with open(f'data/planets.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    if data[id] != None:
        return data[id][0]
    else:
        return False


def getpsd(mail):
    with open('data/accounts.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for user in data:
        if user["mail"] == mail:
            return user["pseudo"]
    return False

# Permet l'update des "/data/mondeX.yaml"
def updateallplanets():
    allpla = {}
    for e in range(1, 10000):
        allpla[e] = None
    li = os.listdir("data/players")
    for e in li:
        with open(f'data/players/{e}', encoding='utf8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        pseudo = e.split(".")[0]
        try:
            for d in data.keys():
                if d != "pinf":
                    if addshield(pseudo, d, 0) > datetime.datetime.now():
                        shield = True
                    else:
                        shield = False
                    allpla[d] = [pseudo, shield]
        except:
            pass
    monde = {}
    for a in range(1, 10000):
        monde[a] = allpla[a]
    with open(f'data/tmp.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(monde, f)
        if "Windows" != platform.system():
            os.system('cp data/tmp.yaml data/planets.yaml')

# Système de récolte des ressources
def updateressource(player):
    onemore = False
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
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

    with open(f'data/players/{player}.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(data, f)
    # Nb ress/h = lvl*10

# Retourne les couts d'amélioration d'un batiment en fonction de son lvl (c,p,h)
def getcostup(bat, lvl):
    cost = 0
    with open('config.yaml', encoding='utf8') as f:
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
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    tmp = getcostup("Carbone", data[int(idpla)]["bat"]["carbone"])
    c = (data[int(idpla)]["bat"]["carbone"],tmp[0],tmp[1],tmp[2])

    tmp = getcostup("Puces", data[int(idpla)]["bat"]["puces"])
    p = (data[int(idpla)]["bat"]["puces"], tmp[0], tmp[1], tmp[2])

    tmp = getcostup("Hydro", data[int(idpla)]["bat"]["hydro"])
    h = (data[int(idpla)]["bat"]["hydro"], tmp[0], tmp[1], tmp[2])

    tmp = getcostup("Rad", data[int(idpla)]["bat"]["rad"])
    rad = (data[int(idpla)]["bat"]["rad"], tmp[0], tmp[1], tmp[2])

    tmp = getcostup("Sp", data[int(idpla)]["bat"]["sp"])
    spaceport = (data[int(idpla)]["bat"]["sp"], tmp[0], tmp[1], tmp[2])

    return {"carbone": c, "puces": p, "hydro": h, "rad": rad, "sp": spaceport}

# Améliora un batiment et retire les ressources du joueur
def upbat(player, batim, couts, plaid):
    if plaid == "*":
        return 0
    addplayerress(player, plaid, (-couts[1],-couts[2],-couts[3]))
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)


    data[int(plaid)]["bat"][batim] += 1

    with open(f'data/players/{player}.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(data, f)

# Récupère le html des vaisseaux dispo en fonction du lvl du sp
def getsp(player, idpla):
    liste = ""
    if idpla == "*":
        return '<h2>Veuillez améliorer votre spatioport pour pouvoir construire des vaisseaux</h3>'
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    lvl = data[int(idpla)]["bat"]["sp"]

    with open(f'config.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    if lvl < 1:
        return '<h2>Veuillez améliorer votre spatioport pour pouvoir construire des vaisseaux</h3>'

    for k,v in data["Vaisseaux"].items():
        tmp = addvaisseau(player, idpla, k, 0)[k]
        if v[3] <= lvl:
            liste += f'''
                <style>
                    #{k} {{
                        background-image: url("../static/imgs/{k}.png");
                        background-repeat: no-repeat;
                        background-size: 20%;
                     }}
                </style>
                <section id="{k}" class="batbuild">
                    <h4>{k}</h4>
                    <p>Possédés : {tmp}</p>
                    <inf class="hide">{k};{tmp};{v[0]};{v[1]};{v[2]};{v[3]};{v[5]}</inf>
                </section>

                '''
    return liste

# Ajoute un vaisseau et retourne la liste de vaisseaux construits
def addvaisseau(player, plaid, vaiss, nb):
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    if vaiss != None:
        try:
            data[int(plaid)]["flotte"][vaiss] = int(nb)+int(data[int(plaid)]["flotte"][vaiss])
        except:
            data[int(plaid)]["flotte"][vaiss] = int(nb)
    re = data[int(plaid)]["flotte"]
    with open(f'data/players/{player}.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(data, f)
    return re

# Retourne le html des vaisseaux construitss
def gethang(player, idpla):
    if idpla == "*":
        return '<h2>Aucun vaisseau sur cette planète</h3>'
    liste = ""
    flotte = addvaisseau(player, idpla, None, None)

    if flotte == {} :
        liste = '<h2>Aucun vaisseau sur cette planète</h3>'
    for k, v in flotte.items():
        if v > 0 :
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
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    data[int(plaid)]["ress"] = (data[int(plaid)]["ress"][0]+ress[0], data[int(plaid)]["ress"][1]+ress[1], data[int(plaid)]["ress"][2]+ress[2])
    re = data[int(plaid)]["ress"]
    with open(f'data/players/{player}.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(data, f)

    return re

# Récupère le cout de création d'un "nb" de vaisseaux
def getvaisscost(vaiss, nb):
    with open('config.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    cost = data["Vaisseaux"][vaiss]
    cost[0] = -cost[0]*int(nb)
    cost[1] = -cost[1]*int(nb)
    cost[2] = -cost[2]*int(nb)
    return cost

# Récupère les infos d'espionage de la planète
def getplainfos(player, plaid):
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return {"ress": data[int(plaid)]["ress"], "flotte": data[int(plaid)]["flotte"]}

# Réucupère toutes les id des planètes d'un joueur
def getallplaid(player):
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    plaids = []
    for k in data:
        if k != "pinf":
            plaids.append(k)
    return plaids

# region Gestion d'attaques
def attackmanager(attaker, aplaid, ptarget, idtarget, flota, flotd):
    with open('config.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    print(addshield(ptarget, idtarget, 0), " | ", datetime.datetime.now())
    if addshield(ptarget, idtarget, 0) > datetime.datetime.now():
        sendmsg(attaker, (
        f"Attaque depuis #{aplaid}",
        f"Vous avez tenté d'attaquer la planète #{idtarget} de {ptarget} cependant il était protégé par un bouclier."
        ))
        return None
    delshield(attaker, aplaid)
    data = data['Vaisseaux']
    powatta = 0
    tata = 0
    powdeff = 10
    for k, v in flota.items():
        powatta += data[k][4] * v
        tata += data[k][5] * v
    for k, v in flotd.items():
        powdeff += data[k][4] * v
    if powatta == 0:
        return None
    if powatta >= powdeff:
        attkwin(attaker, aplaid, ptarget, idtarget)
        return True
    else:
        attklost(attaker, aplaid, ptarget, idtarget, flota)
        return False


def attklost(attaker, aplaid, ptarget, idtarget, flota):
    for k, v in flota.items():
        addvaisseau(attaker, aplaid, k, -v)

    addlog(f"{ptarget}: #{idtarget} s'est défendu contre {attaker}: #{aplaid}")
    sendmsg(attaker, (
        f"Attaque depuis {aplaid}",
        f"L'attaque vers la planète {idtarget} qui appartient à {ptarget} a échouée. Les vaisseaux qui ont été envoyés sont désormais détruits."
    ))

    sendmsg(ptarget, (f"Défense réussie",
                      f"{attaker} vous a attaqué depuis la planète #{aplaid}. Vous avez repoussé l'envahiseur"))


def attkwin(attaker, aplaid, ptarget, idtarget):
    delflotte(ptarget, idtarget)
    addshield(ptarget, idtarget, 48)
    tmp = addplayerress(ptarget, idtarget, (0,0,0))
    print(tmp)
    tmp = (int(tmp[0]/2), int(tmp[1]/2), int(tmp[2]/2))
    addplayerress(ptarget, idtarget, (-tmp[0],-tmp[1],-tmp[2]))
    addplayerress(attaker, aplaid, (tmp[0],tmp[1],tmp[2]))
    sendmsg(attaker, (
        f"Attaque depuis #{aplaid}",
        f"Vous avez attaqué la planète {idtarget} qui appartenait à {ptarget}. Vous lui avez suptilisé {tmp[0]} unités de carbone, {tmp[1]} unitées de puces et {tmp[2]} d'hydrogène."
    ))

    addlog(f"{attaker}: #{aplaid} à pillé {ptarget}: #{idtarget}")
    sendmsg(ptarget, (
        f"Défense échouée",
        f"{attaker} vous a attaqué depuis la planète #{aplaid}. Il vous a suptilisé {tmp[0]} unités de carbone, {tmp[1]} unitées de puces et {tmp[2]} d'hydrogène."
    ))
# endregion

# Supprime la flotte complète d'une planète d'un joueur
def delflotte(player, plaid):
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    data[int(plaid)]["flotte"] = {}
    with open(f'data/players/{player}.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(data, f)


# Retourne le html des messages d'un joueur pour les afficher
def getmsg(player):
    html = ''
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    if len(data["pinf"]["msgs"].items()) == 0:
        html = '<h3>Aucun message</h3>'
        return html
    for k,v in data["pinf"]["msgs"].items():
        html += "<li class='unmsg'><button>"
        html += f"<h3>{v['title']}</h3>"
        html += f"<h6>{v['date'].day}/{v['date'].month}-{v['date'].hour}:{v['date'].minute}</h6>"
        html += f"<p class='hide'>{v['contenu']}</p>"
        html += f"<p class='hide'>{k}</p>"
        html += "</button></li>"
    return html

def sendmsg(player, msg):
    titre = msg[0]
    contenu = msg[1]

    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    idmsg = (
        f'{datetime.datetime.now().month}{datetime.datetime.now().day}{datetime.datetime.now().hour}{datetime.datetime.now().minute}{datetime.datetime.now().second}{datetime.datetime.now().microsecond}'
    )

    data["pinf"]["msgs"][idmsg] = {
        "title": titre,
        "contenu": contenu,
        "date": datetime.datetime.now()
    }

    with open(f'data/players/{player}.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(data, f)


def dellmsg(player, idmsg):
    with open(f'data/players/{player}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    del data["pinf"]["msgs"][idmsg]

    with open(f'data/players/{player}.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(data, f)

# region log system
def addlog(log):
    date = datetime.datetime.now()
    data = []
    try:
        with open(f'logs/{date.day}-{date.month}-{date.year}.yaml', encoding='utf8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except:
        pass

    data.append(f"{date.hour}:{date.minute}:{date.second} >> {log}")

    with open(f'logs/{date.day}-{date.month}-{date.year}.yaml',
              'w',
              encoding='utf8') as f:
        data = yaml.dump(data, f)



def espionmanager(playeratta, plaat, playerdef, pladef):
    if playeratta == playerdef:
        return


    with open(f'data/players/{playeratta}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    attk = data[int(plaat)]["bat"]["sp"]

    with open(f'data/players/{playerdef}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    deff = data[int(pladef)]["bat"]["rad"]

    if attk > deff:
        with open(f'data/players/{playerdef}.yaml', encoding='utf8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        infos = data[int(pladef)]

        sendmsg(playeratta, (
            f"Espionage depuis #{plaat}",
            f"Vous avez espionné la planète {pladef} qui appartenait à {playerdef}. {infos}"
        ))


        # for plaid, dete in data.items():
        #     if plaid != "pinf":
        #         msg.add_field(name=f"\x00", value=f"__-----__", inline=False)
        #         msg.add_field(name=f"Planète #{plaid}", value=f"\x00", inline=False)
        #         msg.add_field(name=f"Ressources", value=f"{dete['ress']}")
        #         msg.add_field(name=f"Batiments", value=f"{dete['bat']}")
        #         msg.add_field(name=f"Flotte", value=f"{dete['flotte']}")


def sendmail(email, sujet, html):
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(mail_email, mail_mdp)
    message = MIMEMultipart("alternative")

    message["Subject"] = sujet
    message["From"] = "across.galaxies.web@gmail.com"
    message["To"] = email

    message.attach(MIMEText(html, "html"))
    s.sendmail("across.galaxies.web@gmail.com", email, message.as_string())
    s.quit()



def resetmdp(email):
    exist = False
    with open('data/accounts.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for e in data:
        if e["mail"] == email:
            exist = True

    if not exist:
        print("Compte innexistant")
        return 0


    letters = string.ascii_lowercase
    token = ''.join(random.choice(letters) for _ in range(10))

    sujet = "Changement de mot de passe"

    textContent = f"""
        <html><body>
        <style>
            h1 {{
                color: red;
                text-align: center;
            }}
        </style>
        <h1>Changement de mot de passe</h1>
        <p>Vous êtres débile, vous avez oublié votre mot de passe ?</p>
        <p>On est sympa, on vous laisse une seconde chance !</p>
        <p>Allez sur ce lien : <a href=http://across-galaxies.com/token>http://across-galaxies.com/token</a>, et rentrer le code ci-dessous.</p>
        <h2>{token}</h2>
        <small>Ce code deviendra invalide à partir de minuit. Si vous n'avez demandé aucun changement de mot de passe, veuillez ignorer ce mail.</small>
        </body></html>
        """

    with open('data/mdplosts.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    data[email] = token


    with open('data/mdplosts.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(data, f)


    print("mail envoyé et token sauvegarder/actualisé")
    sendmail(email, sujet, textContent)