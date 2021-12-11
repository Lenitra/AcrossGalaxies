#!/usr/bin/python
# -*- coding: Utf-8 -*-

import platform
from confi import *
from datetime import datetime
from flask import Flask, render_template, request, redirect, session
import yaml
import across
from reqsql import readsql, reqsql, retbrut

app = Flask(__name__)
app.secret_key = "ahcestcontulaspas"
app.debug = True

def loadconfig():
    tosave = "// carbone - Puces - Hydrogène - lvl du sp - Puissance - Capacité de transport\n"
    with open('config.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for k, v in data["Vaisseaux"].items():
        count = 0
        for e in v:
            tosave += f"let {k}{count} = {e};\n"
            count += 1
        tosave += "\n\n"
    with open('static/js/config.js', 'w', encoding='utf8') as f:
        f.write(tosave)


@app.route('/')
def home():

    print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))

    with open('data/stats.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    try:
        data["hompageimpr"][
        f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"] += 1
    except:
        data["hompageimpr"][
        f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"] = 1
    with open(f'data/stats.yaml','w',encoding='utf8') as f:
        data = yaml.dump(data, f)

    nbinscrits = len(retbrut(f"SELECT Psd FROM Accounts"))
    nbpla = len(retbrut(f"SELECT * FROM Planets WHERE Psd != 'None'"))
    nbpla = f'{nbpla}/{nbinscrits*25}'
    return render_template("index.html", ins = nbinscrits, pla = nbpla)


@app.route("/map", methods=['POST', 'GET'])
def map():
    if across.testpage(session, ("maintenance", "login")):
        return across.testpage(session, ("maintenance", "login"))
    notifmsg = across.checkmsgs(session["player"]["pseudo"])
    liste = ""
    try:
        univers = int(request.form['wunivers'])
    except:
        liste = "<h2>Selection de l'<strong>univers</strong></h2>"
        liste += f"<h4></h4><br>"
        liste += f"<h4></h4><br><br>"
        for id in range(10):
            liste += f'''
                <li class="mappla">
                    <form action="" method="POST" name="{id}">
                        <input type="text" name="wunivers" value ="{id}" class="hide">
                        <button type="submit" style="border: 0; background: transparent">
                            <img src="/static/imgs/univers.png" alt="submit" />
                            <h3>{id}</h3>
                            <h3> &nbsp; </h3>
                        </button>
                    </form>
                </li>
                '''
        return render_template("map.html", plas=liste, notifmsg=notifmsg)

    try:
        galaxie = int(request.form['wgalaxie'])
    except:
        liste = "<h2>Selection de la <strong>galaxie</strong></h2>"
        liste += f"<h4>Univers {univers}</h4>"
        liste += f"<h4>Planètes {univers}xxx</h4>"

        for id in range(10):
            liste += f'''
                <li class="mappla">
                    <form action="" method="POST" name="{id}">
                        <input type="text" name="wunivers" value ="{univers}" class="hide">
                        <input type="text" name="wgalaxie" value ="{id}" class="hide">
                        <button type="submit" style="border: 0; background: transparent">
                            <img src="/static/imgs/galaxie.png" alt="submit" />
                            <h3>{id}</h3>
                            <h3> &nbsp; </h3>
                        </button>
                    </form>
                </li>
                '''
        return render_template("map.html", plas=liste, notifmsg=notifmsg)

    try:
        systeme = int(request.form['wsysteme'])
    except:
        liste = "<h2>Selection du <strong>système</strong></h2>"
        liste += f"<h4>Univers {univers} / Galaxie {galaxie}</h4>"
        liste += f"<h4>Planètes {univers}{galaxie}xx</h4>"
        for id in range(10):
            liste += f'''
                <li class="mappla">
                    <form action="" method="POST" name="{id}">
                        <input type="text" name="wunivers" value ="{univers}" class="hide">
                        <input type="text" name="wgalaxie" value ="{galaxie}" class="hide">
                        <input type="text" name="wsysteme" value ="{id}" class="hide">
                        <button type="submit" style="border: 0; background: transparent">
                            <img src="/static/imgs/sys.png" alt="submit" class="systemesol" />
                            <h3>{id}</h3>
                            <h3> &nbsp; </h3>
                        </button>
                    </form>
                </li>
                '''
        return render_template("map.html", plas=liste, notifmsg=notifmsg)

    start = f'{univers}{galaxie}{systeme}0'
    start = int(start)

    liste = "<h2>Selection de la <strong>planète</strong></h2>"
    liste += f"<h4>Univers {univers} / Galaxie {galaxie} / Système {systeme}</h4>"
    liste += f"<h4>Planètes {univers}{galaxie}{systeme}x</h4>"



    tmp = retbrut(
        f"SELECT Plaid, Psd, Shield FROM Planets WHERE Plaid < {start+10} AND PLAID >= {start}"
    )


    for pl in range(len(tmp)):
        toadd = ""

        id = tmp[pl][0]
        owner = tmp[pl][1]
        if owner != None:
            if tmp[pl][2] > datetime.now():
                shield = True
            else:
                shield = False

        # Si pas de proprio
        if owner == None:
            toadd += f"""
            
                            <li class="mappla">
                                <form action="" method="POST" name="{id}">
                                    <input type="text" name="pla" value ="{id}" class="hide">
                                    <button type="submit" style="border: 0; background: transparent">
                                        <img src="/static/imgs/planet.png" alt="submit" />
                                        <h3>#{id}</h3>
                                        <h3> &nbsp; </h3>
                                    </button>
                                </form>
                            </li>
            """
        else:
            if shield:
                toadd += f'''
                            <li class="mappla">
                                <form action="mapla" method="POST" name="{id}">
                                    <input type="text" name="pla" value ="{id}|{owner}" class="hide">
                                    <button type="submit" style="border: 0; background: transparent">
                                        <img src="/static/imgs/planetcolprot.png" alt="submit" />
                                        <img src="/static/imgs/flag.png" class="flag" alt="submit" />
                                        <h3>#{id}</h3>
                                        <h3 class="conqueror">{owner}</h3>
                                    </button>
                                </form>
                            </li>
                            '''
            else:
                toadd += f'''
                            <li class="mappla">
                                <form action="mapla" method="POST" name="{id}">
                                    <input type="text" name="pla" value ="{id}|{owner}" class="hide">
                                    <button type="submit" style="border: 0; background: transparent">
                                        <img src="/static/imgs/planet.png" alt="submit" />
                                        <img src="/static/imgs/flag.png" class="flag" alt="submit" />
                                        <h3>#{id}</h3>
                                        <h3 class="conqueror">{owner}</h3>
                                    </button>
                                </form>
                            </li>
                            '''
        liste += toadd


    return render_template("map.html", plas=liste, notifmsg=notifmsg)


@app.route("/giveress", methods=['POST', 'GET'])
def giveress():
    across.updateressource(session["player"]["pseudo"])
    return redirect("/jeu")


@app.route("/upbuild", methods=['POST', 'GET'])
def upbuild():
    cout = across.getbats(session["selected"])[request.form['bat']]
    ress = across.addplayerress(session["selected"], (0,0,0))
    if cout[1] <= ress[0] and cout[2] <= ress[1] and cout[3] <= ress[2]:
        across.upbat(request.form['bat'], cout, session["selected"])
    else:
        notifmsg = "Vous n'avez pas assez de ressources pour construire ce batiment"
        session["popup"] = f"""<div id="error_cont"><p>{notifmsg}</p></div>"""
    return redirect("/jeu")


# Intermédiaire pour la construction de vaisseaux
@app.route("/upship", methods=['POST', 'GET'])
def upship():
    vinf = request.form['vinf'] # nom du vaisseau
    nb = request.form['nb']

    cost = across.getvaisscost(vinf, nb)
    ress = across.addplayerress(session["selected"], (0,0,0))
    if ress[0] >= -cost[0] and ress[1] >= -cost[1] and ress[2] >= -cost[2]:
        across.addplayerress(session["selected"], cost)
        nb = int(nb)
        across.addvaisseau(session["selected"], vinf, nb)
    else:
        notifmsg = "Vous n'avez pas assez de ressources pour construire ce(s) vaisseau(x)"
        session["popup"] = f"""<div id="error_cont"><p>{notifmsg}</p></div>"""
    return redirect("/jeu")


@app.route("/mapla", methods=['POST', 'GET'])
def mapla():
    if across.testpage(session, ("maintenance", "login")):
        return across.testpage(session, ("maintenance", "login"))
    notifmsg = across.checkmsgs(session["player"]["pseudo"])
    sel = request.form['pla']
    player = sel.split("|")[1]
    plaid = sel.split("|")[0]
    playerpla = across.getallplaid(session["player"]["pseudo"])
    liste = ""

    liste += f"""<h2>#{plaid} - {player}</h2>
            <h3>A partir de quelle planète effectuer l'action :</h3>
            <div class="select">
            <select name="" id="" onchange="selectpla(this)">"""
    # Selection de la planète
    for e in playerpla:
        liste += f'<option value="{e}">#{e}</option>'
    liste += "</select></div>"

    # Récupération des vaisseaux de chaques planètes
    for e in playerpla:
        liste += f'<div class="grid3c" id="vaisseaux" plaid="{e}">'
        for k, v in across.addvaisseau(e, None, 0).items():
            if v != 0:
                liste += f"""
                    <div>
                        <img src="../static/imgs/{k}.png" alt="">
                        <p>{k} - {v}</p>
                        <input type="number" value="0" name="{k}" id="{k}" min="0" max="{v}">
                    </div>
                """
        liste += "</div>"


    return render_template("mapact.html", plas=liste, notifmsg=notifmsg)

# Page des messages
@app.route("/messages", methods=['POST', 'GET'])
def messages():
    try:
        playerinf = session["player"]["pseudo"]
    except:
        return redirect("/login")
    notifmsg = across.checkmsgs(session["player"]["pseudo"])
    msgs = across.getmsg(session["player"]["pseudo"])
    try:
        print(session["msg"])
    except:
        session["msg"] = 0
    if session["msg"] != 0:
        toaff = across.msgidtohtml(session["player"]["pseudo"], session["msg"])
        if toaff != None:
            # titre date author msg
            toaff = f'''
            
            <section id="msg" class="msg">
            <header>
                <form method='POST' action="/delmsg">
                <input type="number" name="idmsg" value="{session["msg"]}" class='hide'>
                <input type="submit" class="close" value="&times;">
                </form>
                <h1>{toaff[0]}</h1>
            </header>
            <article class="container">
                <p class="date">{toaff[1]}</p>
                <p class="desti"><span id="from">De : </span>{toaff[2]}</p>
                <hr>
                {toaff[3]}
            </article>
            </section>
            
            '''
            session["msg"] = 0

        else:
            toaff = ""
            session["msg"] = 0
    else:
        toaff = ""
    return render_template("messages.html", msgs = msgs, notifmsg = notifmsg, toaff = toaff)

# Intermédiaire pour supprimer un message
@app.route("/delmsg", methods=['POST', 'GET'])
def delmsg():
    id = request.form['idmsg']
    across.dellmsg(session["player"]["pseudo"], int(id))
    return redirect("/messages")

# Intermédiaire pour lancer une attaque
@app.route("/atta", methods=['POST', 'GET'])
def atta():
    # region Récupération des éléments

    action = request.form['action']
    plaat = int(request.form['platta'])
    pladef = int(request.form['platarg'])

    croiseur = int(request.form['Croiseur'])
    nanosonde = int(request.form['Nano-Sonde'])
    cargo = int(request.form['Cargo'])
    victoire = int(request.form['Victoire'])
    colonisateur = int(request.form['Colonisateur'])

    carbone = int(request.form['Carbone'])
    puces = int(request.form['Puces'])
    hydro = int(request.form['Hydro'])

    playeratta = across.checkpla(plaat)
    playerdef = across.checkpla(pladef)
    flotdef = across.addvaisseau(pladef, None, None)
    flotatta = {
        "Croiseur": croiseur,
        "Nanosonde": nanosonde,
        "Victoire": victoire,
        "Colonisateur": colonisateur,
        "Cargo": cargo
    }

    ress = (carbone, puces, hydro)


    # endregion

    # region Check si le joueur n'as pas envoyé plus de vaisseaux qu'il n'a
    tmp = across.addvaisseau(plaat, None, None)
    for k,v in flotatta.items():
        if flotatta[k] > tmp[k]:
            flotatta[k] = tmp[k]
    # endregion



    if action == 'Attaquer':
        if playeratta == playerdef:
            return redirect("/map")
        resultat = across.attackmanager(playeratta, plaat,
                                        playerdef,pladef , flotatta, flotdef)

    if action == "Espionner":
        if playeratta == playerdef:
            return redirect("/map")
        print("espionnage !!!!")
        across.espionmanager(playeratta, plaat, playerdef, pladef)

    if action == "Docker":
        if plaat == pladef:
            return redirect("/map")
        print("docker !!!!")
        across.dockermanager(flotatta, plaat, pladef)
        across.sendmsg(
            playeratta,
            f"Vous avez envoyé des vaisseaux vers la planète #{pladef}", f'''
                <style>
                .inmsgtextclol {{
                    text-align: center;
                }}
                </style>
                <h3 class="inmsgtextclol">Vaisseaux envoyés<br>Sur : #{pladef} ({playerdef})<br>Depuis : #{plaat} ({playeratta})</h3>
                <p class="inmsgtextclol">Croiseur : {flotatta["Croiseur"]}</p>
                <p class="inmsgtextclol">Nanosonde : {flotatta["Nanosonde"]}</p>
                <p class="inmsgtextclol">Cargo : {flotatta["Cargo"]}</p>
                <p class="inmsgtextclol">Victoire : {flotatta["Victoire"]}</p>
                <p class="inmsgtextclol">Colonisateur : {flotatta["Colonisateur"]}</p>
            ''', "Système")
        across.sendmsg(
            playerdef,
            f"Vous avez reçu des vaisseaux depuis la planète #{plaat}", f'''
                <style>
                .inmsgtextclol {{
                    text-align: center;
                }}
                </style>
                <h3 class="inmsgtextclol">Vaisseaux reçus<br>Sur : #{pladef} ({playerdef})<br>Depuis : #{plaat} ({playeratta})</h3>
                <p class="inmsgtextclol">Croiseur : {flotatta["Croiseur"]}</p>
                <p class="inmsgtextclol">Nanosonde : {flotatta["Nanosonde"]}</p>
                <p class="inmsgtextclol">Cargo : {flotatta["Cargo"]}</p>
                <p class="inmsgtextclol">Victoire : {flotatta["Victoire"]}</p>
                <p class="inmsgtextclol">Colonisateur : {flotatta["Colonisateur"]}</p>
            ''', "Système")
    return redirect("/messages")

# Intermédiaire pour update les ressources
@app.route("/updatedata", methods=['POST', 'GET'])
def updatedata():
    session['selected'] = request.form['pla']
    return redirect("/jeu")

# Page principale du jeu (colonie)
@app.route("/jeu",  methods=['POST', 'GET'])
def jeu():
    if across.testpage(session, ("maintenance", "login")):
        return across.testpage(session, ("maintenance", "login"))

    shield = across.addshield(session["selected"], 0)
    if shield < datetime.now():
        shield = "Aucun bouclier"
    else:
        shield = f"{shield.day}/{shield.month} - {shield.hour}h"

    listeplanetes = across.getplanetslist(session["player"]["pseudo"])
    power = across.getpower(across.addvaisseau(session['selected'], None,0))
    spaceport = across.getsp(session['selected'])
    batiments = across.getbats(session["selected"])
    ressources = across.addplayerress(session["selected"], (0, 0, 0))
    notifmsg = across.checkmsgs(session["player"]["pseudo"])

    try:
        popup = session["popup"]
        session["popup"] = ""
    except:
        popu = ""

    return render_template("jeu.html",
                           listpla=listeplanetes,
                           ress=ressources,
                           pname=session['selected'],
                           shield=shield,
                           bat=batiments,
                           spaceport=spaceport,
                           power=power,
                           notifmsg = notifmsg,
                           popup = popup)


# Vérifie la connexion
@app.route("/readmsg", methods=['POST', 'GET'])
def readmsg():
    session["msg"] = request.form['idmsg']
    return redirect("/messages")

# Vérifie l'inscription
@app.route("/checkreg", methods=['POST', 'GET'])
def checkreg():
    mail = request.form['r_mail']
    pseudo = request.form['r_pseudo']
    mdp = request.form['r_mdp']
    mdp2 = request.form['r_mdp_c']
    capcha = request.form['captcha'].upper()
    truecapt = request.form['truecapt']



    if capcha != truecapt:
        session['logerror'] = "Captcha invalide"
        return redirect("/login")


    if mdp != mdp2:
        session['logerror'] = "Confirmation de mot de passe incorrecte"
        return redirect("/login")

    regresult = across.register(mail, mdp, pseudo)

    if regresult == 255:
        session["player"] = {"pseudo": "", "mail": ""}
        session["player"]["mail"] = mail
        session["player"]["pseudo"] = pseudo
        session["selected"] = readsql(f"SELECT Plaid FROM Planets WHERE Psd = '{pseudo}';")[0]

        return redirect("/jeu")
    if regresult == 0:
        session['logerror'] = "Veuillez remplir tout les champs"
    if regresult == 1:
        session['logerror'] = "Mail non valide"
    if regresult == 2:
        session['logerror'] = "Mail déjà utilisé"
    if regresult == 3:
        session['logerror'] = "Pseudo déjà utilisé"
    if regresult == 4:
        session['logerror'] = "Pseudo non conforme"
    if regresult == 5:
        session['logerror'] = "Mot de passe non conforme"


    return redirect("/login")

# Vérifie la connexion
@app.route("/checklog", methods=['POST', 'GET'])
def checklog():

    mail = request.form['l_mail']
    mdp = request.form['l_mdp']
    psd = across.connect(mail, mdp)
    if psd != False:
        session["player"] = {}
        session["player"]["mail"] = mail
        session["player"]["pseudo"] = psd


        session["selected"] = readsql(f"SELECT Plaid FROM Planets WHERE Psd = '{psd}';")[0]


        session.pop('logerror', None)
        return redirect("/jeu")
    else:
        session["logerror"] = "Identifiant ou mot de passe incorect"
        return redirect("/login")


@app.route("/login", methods=['GET', 'POST'])
def login():

    session["player"] = {}
    try:
        error = session["logerror"]
        erreur = f"""<div id="error_cont"><p>{error}</p></div>"""
    except:
        erreur = ""

    with open('data/capt.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    captcha = data
    return render_template("logreg.html", error = erreur, captcha = captcha)


@app.route("/forgmail", methods=['GET', 'POST'])
def forgmail():
    across.resetmdp(request.form['forgmail'])
    return redirect("/login")


@app.route("/changemdp", methods=['GET', 'POST'])
def changemdp():

    old = request.form['old']
    new = request.form['new']
    conf = request.form['new']
    if conf != new or not across.connect(session["player"]["mail"], old):
        return redirect("/options")

    across.changepass(session["player"]["mail"], new)

    return redirect("/options")


@app.route("/options", methods=['GET', 'POST'])
def options():
    if across.testpage(session, ("maintenance", "login")):
        return across.testpage(session, ("maintenance", "login"))
    notifmsg = across.checkmsgs(session["player"]["pseudo"])

    return render_template("options.html", notifmsg=notifmsg)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 404


@app.route("/togglemaintenance", methods=['GET', 'POST'])
def togglemaintenance():
    with open('data/stats.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    if data["Maintenance"]:
        data["Maintenance"] = False
    else:
        data["Maintenance"] = True

    with open(f'data/stats.yaml','w',encoding='utf8') as f:
        data = yaml.dump(data, f)


    return redirect("/admin")


@app.route("/maintenance", methods=['GET', 'POST'])
def maintenance():
    return render_template("maintenance.html")


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    try:
        print(session['player']['pseudo'])
    except:
        return redirect("/login")
    if readsql(f"SELECT Staff FROM PInf WHERE Psd = '{session['player']['pseudo']}';")[0] != 5:
        return redirect("/")
    else:

        now = datetime.now()

        # region Stats
        with open('data/stats.yaml', encoding='utf8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        impr = [0,0,0]
        for k, v in data["hompageimpr"].items():
            if k.split("-")[0] == f"{now.year}":
                impr[0] += v
            if k.split("-")[1] == f"{now.month}":
                impr[1] += v
            if k.split("-")[2] == f"{now.day}":
                impr[2] += v
        #endregion

        # region Logs
        loghtml = f"<h2>{now.year}-{now.month}-{now.day}</h2>"
        try:
            with open(f'logs/{now.day}-{now.month}-{now.year}.yaml',
                    encoding='utf8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
            for log in data:
                loghtml += f"""<div class="log">{log}</div>"""
        except:
            loghtml = "<div class='log'>Pas de logs aujourd'hui</div>"
        #endregion

        # region Options>Maintenance
        with open('data/stats.yaml', encoding='utf8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        if data["Maintenance"]:
            maintenance = "Maintenance active"
        else:
            maintenance = "Maintenance inactive"
        # endregion

        return render_template("admin.html",impr = impr, logs = loghtml, maintenance = maintenance)



if __name__ == '__main__':
    loadconfig()

    if platform.system() != "Windows":
        website_url = 'across-galaxies.fr:80'
        app.config['SERVER_NAME'] = website_url

    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_NAME'] = "BonsCookies"

    app.run()
