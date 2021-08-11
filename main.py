#!/usr/bin/python
# -*- coding: Utf-8 -*-

from datetime import datetime
from threading import Semaphore
from flask import Flask, render_template, request, redirect, session
import socket
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
    with open(f'data/planets.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for id in range(ref,ref+25):
        # print(id , " - " , data[int(id)])
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
    for p in playerpla:

        for vai, nb in across.addvaisseau(session["player"]["pseudo"], p, None, 0).items():
            try:
                flotte[vai] += nb
            except:
                flotte[vai] = nb

    infos = f'<h1>{plaid} - {player}</h1>'
    for k,v in flotte.items():
        infos += f"""
        <ul>
            <li><img src='static/imgs/{k}.png'></li>
            <li><h3>{v}</h3></li>
        </ul>
    """
    # <p>{vadispo}</p>
    # <button>ATTAQUER</button>
    # <button>TRANSPORTER</button>
    # <button>DOCKER</button>
    # <button>CONQUÉRIR</button>
    liste = infos
    return render_template("map.html", plas=liste)

@app.route("/updatedata", methods=['POST', 'GET'])
def updatedata():
    session['selected'] = request.form['pla']
    return redirect("/jeu")


@app.route("/jeu",  methods=['POST', 'GET'])
def jeu():
    try:
        session["player"]
    except:
        return redirect("/login")
    with open(f'data/players/{session["player"]["pseudo"]}.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for e in data:
        if e != 'pinf':
            session["selected"] = e
            break 
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
        session['selected'] = "*"
        return redirect("/jeu")
    else:
        return redirect("/login")


@app.route("/login", methods=['GET', 'POST'])
def login():
    session["player"] = {"pseudo": "", "mail": ""}
    return render_template("logreg.html")


if __name__ == '__main__':
    app.run(host=socket.gethostname(), port=8080)
