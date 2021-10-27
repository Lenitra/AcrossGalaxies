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
from captcha.image import ImageCaptcha
import reqsql




def encode(message: str):
    key = secret_key
    message = bytes(message, "utf-8")
    return Fernet(key).encrypt(message)


def decode(token: bytes):
    key = secret_key
    return (Fernet(key).decrypt(token)).decode("utf-8")


def connect(mail, mdp):
    mailver = reqsql.readsql(f"SELECT Mail FROM Accounts WHERE Mail='{mail}';")
    if mailver == None:
        return False
    if decode(bytes(reqsql.readsql(f"SELECT Mdp FROM Accounts WHERE Mail='{mail}';")[0].split("'")[1], "utf-8")) == mdp:
        return reqsql.readsql(
            f"SELECT Psd FROM Accounts WHERE Mail='{mail}';")[0]
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
    while reqsql.readsql(f"SELECT Psd FROM Planets WHERE Plaid={plaid};")[0] != None:
        plaid = random.randint(1, 9999)


    # with open('data/accounts.yaml', encoding='utf8') as f:
    #     users = yaml.load(f, Loader=yaml.FullLoader)

    if mail == "" or mdp == "" or pseudo == "":
        return 0

    if "." in mail.split("@")[1]:
        pass
    else:
        return 2

    if reqsql.readsql(f"SELECT Mail FROM Accounts WHERE Mail='{mail}';") != None:
        return 2

    if reqsql.readsql(
            f"SELECT Psd FROM Accounts WHERE Psd='{pseudo}';") != None:
        return 3

    if len(mdp) <= 5:
        return 5

    else:
        mdp = encode(mdp)
        # Accounts : Permet la connexion avec Psd | Mail | Mdp
        reqsql.reqsql(f'INSERT INTO Accounts VALUES ("{pseudo}", "{mail}", "{mdp}");')
        # Planets : liste de toutes les planètes avec TOUTES les données internes à chaques planètes

        reqsql.reqsql(
            f'''UPDATE Planets SET Psd = "{pseudo}", Shield = "{datetime.datetime.now()}" ,Ress1 = 250, Ress2 = 250, Ress3 = 250, carbone = 1, puces = 1, hydro = 1, sp = 1, rad = 1, Croiseur = 0, Nanosonde = 0, Cargo = 0, Victoire = 0, Colonisateur = 0 WHERE Plaid = {plaid};'''
        )

        reqsql.reqsql(
            f'''INSERT INTO PInf VALUES ("{pseudo}", "{datetime.datetime.now()}", "{datetime.datetime.now()}", 0);''')

        idmsg = (
            f'{datetime.datetime.now().month}/{datetime.datetime.now().day}{datetime.datetime.now().hour} {datetime.datetime.now().minute}:{datetime.datetime.now().second}{datetime.datetime.now().microsecond}'
        )

        date = f"{datetime.datetime.now().month}/{datetime.datetime.now().day} {datetime.datetime.now().hour}:{datetime.datetime.now().minute}"

        user = {
            idmsg: {
                "title": "Bienvenue !",
                "msg":"<p>Bienvenue sur le jeu Across Galaxies ! \nSi vous avez des question je vous prie de rejoindre le serveur discord. En vous souhaitant un bon jeu ! \nCordialement l'équipe de Across-Galaxies.</p>",
                "author": "Système",
                "date": date
            }
        }

        with open(f'data/msgs/{pseudo}.yaml', 'w', encoding='utf8') as f:
            data = yaml.dump(user, f)

        # addlog(f"{pseudo} s'est inscrit avec le mail {mail}")
        # addshield(pseudo, plaid, 48)
        return 255

# Ajoute un shield effectif de "hours" heures après l'appel de la fonction
def addshield(plaid, hours):

    shield = 0

    if hours != None:

        myDate = datetime.datetime.now()
        td = datetime.timedelta(hours = hours)
        shield = myDate + td
        reqsql.reqsql(f"UPDATE Planets SET Shield = '{shield}' WHERE Plaid = {plaid};")
    else:
        shield = reqsql.readsql(f"SELECT Shield FROM Planets WHERE Plaid = {plaid}")
    return shield



def delshield(plaid):
    reqsql.reqsql(
        f"UPDATE Planets SET Shield = '{datetime.datetime.now()}' WHERE Plaid = {plaid};"
    )


def getplanetslist(player):
    plalist=''

    pll = reqsql.retbrut(f"SELECT Plaid FROM Planets WHERE Psd = 'Lenitra';")

    for pl in pll:
        k = pl[0]
        v = addplayerress(pl, None)
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
        else:
            os.system('copy data/tmp.yaml data')

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
def getbats(idpla):

    lvl = reqsql.readsql(
        f"SELECT carbone FROM Planets WHERE Plaid = {idpla}")[0]
    tmp = getcostup("Carbone", lvl)
    c = (lvl,tmp[0],tmp[1],tmp[2])

    lvl = reqsql.readsql(f"SELECT puces FROM Planets WHERE Plaid = {idpla}")[0]
    tmp = getcostup("Puces", lvl)
    p = (lvl, tmp[0], tmp[1], tmp[2])

    lvl = reqsql.readsql(f"SELECT hydro FROM Planets WHERE Plaid = {idpla}")[0]
    tmp = getcostup("Hydro", lvl)
    h = (lvl, tmp[0], tmp[1], tmp[2])

    lvl = reqsql.readsql(f"SELECT rad FROM Planets WHERE Plaid = {idpla}")[0]
    tmp = getcostup("Rad", lvl)
    rad = (lvl, tmp[0], tmp[1], tmp[2])

    lvl = reqsql.readsql(f"SELECT sp FROM Planets WHERE Plaid = {idpla}")[0]
    tmp = getcostup("Sp", lvl)
    spaceport = (lvl, tmp[0], tmp[1], tmp[2])

    return {"carbone": c, "puces": p, "hydro": h, "rad": rad, "sp": spaceport}

# Améliora un batiment et retire les ressources du joueur
def upbat(player, batim, couts, plaid):
    if plaid == "*":
        return 0
    addplayerress(plaid, (-couts[1],-couts[2],-couts[3]))
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

    lvl = reqsql.readsql("SELECT sp FROM Planets WHERE Plaid=1;")[0]

    with open(f'config.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    if lvl < 1:
        return '<h2>Veuillez améliorer votre spatioport pour pouvoir construire des vaisseaux</h3>'

    for k,v in data["Vaisseaux"].items():
        tmp = addvaisseau(idpla, k, 0)[k]
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
                    <inf class="hide">{k};{tmp};{v[0]};{v[1]};{v[2]};{v[3]};{v[4]};{v[5]}</inf>
                </section>

                '''
    return liste

# Ajoute un vaisseau et retourne la liste des vaisseaux construits
def addvaisseau(plaid, vaiss, nb):
    if vaiss != None and nb != None:
        # ajouter un vaisseau
        pass

    vaisseaux = reqsql.readsql(f"SELECT Croiseur, NanoSonde, Cargo, Victoire, Colonisateur  FROM Planets WHERE Plaid={plaid};")
    re = {"Croiseur": vaisseaux[0],
     "Nanosonde": vaisseaux[1],
     "Cargo": vaisseaux[2],
     "Victoire": vaisseaux[3],
     "Colonisateur": vaisseaux[4]
     }
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
def addplayerress(plaid, ress):
    if ress != None and ress !=0:
        reqsql.reqsql(
            f"UPDATE Planets SET Ress1={ress[0]}, Ress2={ress[1]}, Ress3={ress[2]} WHERE Plaid = {plaid};"
        )

    re = reqsql.readsql(f"SELECT Ress1, Ress2, Ress3 FROM Planets WHERE Plaid = 9999;")

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

def getpower(flotte):
    power = 0
    with open('config.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    data = data["Vaisseaux"]
    for k, v in flotte.items():
        power += data[k][4] * v
    return power

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
    powdeff = 10
    for k, v in flota.items():
        powatta += data[k][4] * v
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

def sendmsg(player, title, msg, author):

    try:
        with open(f'data/msgs/{player}.yaml', encoding='utf8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except:
        data = []

    idmsg = (
        f'{datetime.datetime.now().month}{datetime.datetime.now().day}{datetime.datetime.now().hour}{datetime.datetime.now().minute}{datetime.datetime.now().second}{datetime.datetime.now().microsecond}'
    )

    date = f"{datetime.datetime.now().month}/{datetime.datetime.now().day} {datetime.datetime.now().hour}:{datetime.datetime.now().minute}"


    user = {
        idmsg: {
            "title": title,
            "msg": msg,
            "author": author,
            "date": date
        }
    }


    with open(f'data/msgs/{player}.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(user, f)


    # data["pinf"]["msgs"][idmsg] = {
    #     "title": titre,
    #     "contenu": contenu,
    #     "date": datetime.datetime.now()
    # }

    # with open(f'data/players/{player}.yaml', 'w', encoding='utf8') as f:
    #     data = yaml.dump(data, f)


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
        infos = data[int(pladef)]

        sendmsg(playeratta, (
            f"Espionage depuis #{plaat}",
            f"Vous avez espionné la planète {pladef} qui appartenait à {playerdef}. {infos}"
        ))


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
    password = False
    with open('data/accounts.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for e in data:
        if e["mail"] == email:
            password = decode(e["mdp"])

    if not password:
        print("Compte innexistant")
        return 0



    sujet = "Changement de mot de passe"

    textContent = f"""
    <html>

    <head>
    <style>
        @font-face {{
            font-family: "Titres";
            src: url("../static/fonts/Aileron.otf")
        }}

        @font-face {{
            font-family: "Textes";
            src: url("../static/fonts/neuro.ttf")
        }}
        body{{
            background-color: gray;
            color: white;
        }}
        *{{
            color: white;
        }}
        .central{{
            width: 50%;
            min-width: 50%;
            background: linear-gradient(to top, #1b2735, #19202b, #151a22, #111319, #090a0f);
            border: 1px solid black ;
            margin: auto;
            height: 100%;
        }}
        h1{{
            font-family: "Textes";
            color: white;
            font-size: 2vw;
            text-align: center;
            background-color: rgba(98, 101, 103, 0.4);
            border-radius: 16% 3% ;
            margin: 1% auto;
        }}
        #attention{{
            color: red;
            font-weight: bold;
        }}
        h3{{
            text-align: center;
            background-color: #01568b;
            border: 1px solid black;
            width: auto;
            margin: 5vh 10vw;
            border-radius: 15%;
            font-size: 2vw;
            font-family: "Textes";
        }}
        p{{
            margin: 1vw ;
            padding-top: 2vh;
            text-align: center;
        }}
        #norm{{
            text-align: left;
        }}
    </style>
    </head>

    <body>

    <section class="central">
        <article>
                <h1>Oubli du mot de passe</h1>
                <p>Vous avez votre mot de passe de votre compte Across-Galaxies.</p>
                <p>Comme on est hyper sympa on vous laisse une seconde chance.</p>
                <p><i>{password}</i></p>
                <hr>
                <p id="norm"><span id="attention">ATTENTION</span> : Pour des raisons de sécurité nous vous invitons à re-changer votre mot de passe en jeu dans l'onglet "options". Si vous n'avez demandé aucun changement de mot de passe, veuillez ignorer ce mail.</p>
        </article>
    </section>
    
    </body></html>
    """

    sendmail(email, sujet, textContent)
    print("Mail envoyé")


def updatecapt(text):

    image = ImageCaptcha(width=280, height=90)

    capt_text = text
    image.generate(capt_text)

    image.write(capt_text, "static/imgs/CAPTCHA.png")
    with open(f'data/capt.yaml', 'w', encoding='utf8') as f:
        text = yaml.dump(text, f)


def changepass(mail, np):

    mdp = encode(np)
    pseudo = getpsd(mail)
    nd = []


    with open('data/accounts.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for users in data:
        tmp = {}
        ok = False
        for k,v in users.items():
            tmp[k]=v
            if k == "mail" and v == mail:
                ok = True
        if ok:
            tmp["mdp"] = encode(np)
        nd.append(tmp)





    with open('data/accounts.yaml', 'w') as f:
        data = yaml.dump(nd, f)

    addlog(f"{pseudo} à changé son mot de passe")
    sendmsg(pseudo, (
        "Changement de mot de passe",
        "Votre mot de passe à bien été changé."
    ))
    return 255


def checkmsgs(psd):
    if getmsg(psd) == '<h3>Aucun message</h3>':
        return 0
    return 1