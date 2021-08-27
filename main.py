#!/usr/bin/python
# -*- coding: Utf-8 -*-

from datetime import datetime
from os import access
from threading import Semaphore
from flask import Flask, render_template, request, redirect, session
import yaml
import across

app = Flask(__name__)
app.secret_key = "ahcestcontulaspas"
app.debug = True


@app.route('/')
def home():
    # affichage
    return render_template("index.html")


@app.route("/selpla", methods=['POST', 'GET'])
def selpla():
    return redirect("/jeu")


@app.route("/map", methods=['POST', 'GET'])
def map():
    try:
        ref = int(request.form['wmap'])
    except:
        liste = ""
        return render_template("map.html", plas=liste)

    if ref >= 9999:
        ref = 9999 - 12

    if ref < 12:
        ref = 0
    else:
        ref -= 12
        print(ref)


    liste = ""
    with open(f'data/planets.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for id in range(ref,ref+25):
        if data[int(id)] == None:
            liste += f'''
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
                '''
        else:
            liste += f'''
                <li class="mappla">
                    <form action="mapla" method="POST" name="{id}">
                        <input type="text" name="pla" value ="{id}|{data[int(id)]}" class="hide">
                        <button type="submit" style="border: 0; background: transparent">
                            <img src="/static/imgs/planetcol.png" alt="submit" />
                            <h3>#{id}</h3>
                            <h3 class="conqueror">{data[int(id)]}</h3>
                        </button>
                    </form>
                </li>
                '''


    return render_template("map.html", plas = liste)


@app.route("/giveress", methods=['POST', 'GET'])
def giveress():
    across.updateressource(session["player"]["pseudo"])
    return redirect("/jeu")


@app.route("/upbuild", methods=['POST', 'GET'])
def upbuild():
    cout = across.getbats(session["player"]["pseudo"],
                          session["selected"])[request.form['bat']]
    ress = across.addplayerress(session["player"]["pseudo"], session["selected"], (0,0,0))
    if cout[1] <= ress[0] and cout[2] <= ress[1] and cout[3] <= ress[2]:
        across.upbat(session["player"]["pseudo"], request.form['bat'], cout, session["selected"])
    return redirect("/jeu")


# Intermédiaire pour la construction de vaisseaux
@app.route("/upship", methods=['POST', 'GET'])
def upship():
    vinf = request.form['vinf']
    nb = request.form['nb']
    cost = across.getvaisscost(vinf, nb)
    ress = across.addplayerress(session["player"]["pseudo"], session["selected"], (0,0,0))
    if ress[0] >= -cost[0] and ress[1] >= -cost[1] and ress[2] >= -cost[2]:
        across.addplayerress(session["player"]["pseudo"], session["selected"], cost)
        across.addvaisseau(session["player"]["pseudo"], session["selected"], vinf, nb)
    return redirect("/jeu")


@app.route("/mapla", methods=['POST', 'GET'])
def mapla():
    sel = request.form['pla']
    player = sel.split("|")[1]
    plaid = sel.split("|")[0]
    playerpla = across.getallplaid(session["player"]["pseudo"])
    flotte = {}
    liste = ""
    liste += '<form action="/atta" method="POST" name="atta">'
    liste += "<div class='firstgridd'>"
    liste += f'<h1 class="mapti">#{plaid} - {player}</h1>'
    liste += "<section>"
    liste += "<h3>A partir de quelle planète executer une action :</h3>"
    liste += "<br>"
    liste += '<select name="attaplaid" onchange="selectpla(this)">'
    liste += "<option>Selectionner</option>"
    for e in playerpla:
        liste += f"<option>#{e}</option>"
    liste += "</select>"
    liste += "</section>"
    liste += "</div>"

    liste += f'''<input type="text" class="hide" name="plaid" value="{plaid}">'''
    liste += "<div class='secondgrid'>"
    for e in playerpla:
        for k, v in across.addvaisseau(session["player"]["pseudo"], e, None, 0).items():
            if v != 0:
                liste += f"""
                    <section class="vaissmap hide" id="{e}">
                        <img src='static/imgs/{k}.png'>
                        <h3>{k} : {v}</h3>
                    </section>
                """
    liste += "</div>"
    liste += """
            <br>
            <select name="select" onchange="selectaction(this)">
                <option>Action</option>
                <option>Attaquer</option>
                <option>Espioner</option>
                <option>Docker</option>
                <option>Transporter</option>
                <option>Coloniser</option>
            </select>"""
    liste += '<button type="submit"><h3>Valider</h3></button>'
    liste += "</form>"
    return render_template("map.html", plas=liste)

# Page des messages
@app.route("/messages", methods=['POST', 'GET'])
def messages():
    msgs = across.getmsg(session["player"]["pseudo"])
    return render_template("messages.html", msgs = msgs)

# Intermédiaire pour supprimer un message
@app.route("/delmsg", methods=['POST', 'GET'])
def delmsg():
    id = request.form['idmsg']
    across.dellmsg(session["player"]["pseudo"], id)
    return redirect("/messages")

# Intermédiaire pour lancer une attaque
@app.route("/atta", methods=['POST', 'GET'])
def atta():
    # region Récupération des éléments
    action = request.form['select']
    pladef = int(request.form['plaid'])
    if request.form['attaplaid'] == "Selectionner":
        return redirect("/map")

    plaatta = int(request.form['attaplaid'].split("#")[1])
    player = across.checkpla(pladef)
    pflo = across.addvaisseau(session["player"]['pseudo'], plaatta, None, None)
    # endregion
    if action == 'Attaquer':
        if player == session["player"]["pseudo"]:
            return redirect("/map")
        try:
            Croiseur = int(request.form['Croiseur'])
            if Croiseur > pflo["Croiseur"]:
                Croiseur = pflo["Croiseur"]
        except:
            Croiseur = 0
        try:
            Nano_Sonde = int(request.form['Nano-Sonde'])
            if Nano_Sonde > pflo["Nano-Sonde"]:
                Nano_Sonde = pflo["Nano-Sonde"]
        except:
            Nano_Sonde = 0
        try:
            Cargo = int(request.form['Cargo'])
            if Nano_Sonde > pflo["Nano-Sonde"]:
                Nano_Sonde = pflo["Nano-Sonde"]
        except:
            Cargo = 0
        try:
            Victoire = int(request.form['Victoire'])
            if Victoire > pflo["Victoire"]:
                Victoire = pflo["Victoire"]
        except:
            Victoire = 0
        try:
            Colonisateur = int(request.form['Colonisateur'])
            if Colonisateur > pflo["Colonisateur"]:
                Colonisateur = pflo["Colonisateur"]
        except:
            Colonisateur = 0
        flotatta = {
            "Croiseur": Croiseur,
            "Nano-Sonde": Nano_Sonde,
            "Victoire": Victoire,
            "Colonisateur": Colonisateur,
            'Cargo': Cargo
        }
        deff = across.addvaisseau(player, pladef, None, None)
        resultat = across.attackmanager(session["player"]["pseudo"], plaatta , player,
                             pladef, flotatta, deff)
    if action == "Espioner":
        pass
    return redirect("/map")

# Intermédiaire pour update les ressources
@app.route("/updatedata", methods=['POST', 'GET'])
def updatedata():
    session['selected'] = request.form['pla']
    return redirect("/jeu")

# Page principale du jeu (colonie)
@app.route("/jeu",  methods=['POST', 'GET'])
def jeu():
    try:
        session["player"]
    except:
        return redirect("/login")

    shield = across.addshield(session["player"]["pseudo"], session['selected'], 0)
    if shield < datetime.now():
        shield = "Aucun bouclier"
    else:
        shield = f"{shield.day}/{shield.month} - {shield.hour}h"
    vaisseaux = across.gethang(session["player"]["pseudo"], session['selected'])
    spaceport = across.getsp(session["player"]["pseudo"],session['selected'])
    batiments = across.getbats(session["player"]["pseudo"], session["selected"])
    ressources = across.addplayerress(session["player"]["pseudo"],session["selected"], (0, 0, 0))
    listeplanetes = across.getplanetslist(session["player"]["pseudo"])
    return render_template(
        "jeu.html",
        listpla=listeplanetes,
        ress=ressources,
        pname=session['selected'],
        shield = shield,
        bat=batiments,
        spaceport=spaceport,
        hang=vaisseaux
        )


# Vérifie la connexion
@app.route("/checkreg", methods=['POST', 'GET'])
def checkreg():
    mail = request.form['r_mail']
    pseudo = request.form['r_pseudo']
    mdp = request.form['r_mdp']
    if across.register(mail, mdp, pseudo) == 255:
        session["player"] = {"pseudo": "", "mail": ""}
        session["player"]["mail"] = mail
        session["player"]["pseudo"] = pseudo
        session['selected'] = "*"
        return redirect("/jeu")
    return redirect("/login")

# Vérifie la connexion
@app.route("/checklog", methods=['POST', 'GET'])
def checklog():
    session["player"] = {"pseudo": "", "mail": ""}
    mail = request.form['l_mail']
    mdp = request.form['l_mdp']
    if across.connect(mail, mdp) != False:
        session["player"]["mail"] = mail
        session["player"]["pseudo"] = across.getpsd(mail)
        with open(f'data/players/{session["player"]["pseudo"]}.yaml', encoding="utf8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        for e in data:
            print(e, session["selected"])
            if e != 'pinf':
                session["selected"] = e
                break
        return redirect("/jeu")
    else:
        return redirect("/login")


@app.route("/login", methods=['GET', 'POST'])
def login():
    session["player"] = {"pseudo": "", "mail": ""}
    return render_template("logreg.html")


@app.route("/options", methods=['GET', 'POST'])
def options():
    return render_template("options.html")



@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
