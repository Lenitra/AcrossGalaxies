#!/usr/bin/python
# -*- coding: Utf-8 -*-

from threading import Semaphore
from flask import Flask, render_template, request, redirect, session
import socket
import os
import across

app = Flask(__name__)
app.secret_key = "ahcestcontulaspas"
app.debug = True

#


@app.route('/')
def home():
    # affichage
    return render_template("index.html")


@app.route("/giveress", methods=['POST', 'GET'])
def giveress():
    across.updateressource(session["player"]["pseudo"])
    return redirect("/jeu")


@app.route("/upbuild", methods=['POST', 'GET'])
def upbuild():
    cout = session["bat"][request.form['bat']]
    ress = across.addplayerress(session["player"]["pseudo"], session["selected"], (0,0,0))
    if cout[1] <= ress[0] and cout[2] <= ress[1] and cout[3] <= ress[2]:
        across.upbat(session["player"]["pseudo"], request.form['bat'], cout, session["selected"])
    return redirect("/jeu")


# Vérifie la connexion
@app.route("/upship", methods=['POST', 'GET'])
def upship():

    vinf = request.form['vinf'].split(",")
    nb = request.form['nb']
    cost = (-int(nb)*int(vinf[1]), -int(nb)*int(vinf[2]), -int(nb)*int(vinf[3]))
    ress = across.addplayerress(session["player"]["pseudo"], session["selected"], (0,0,0))
    if ress[0] >= -cost[0] and ress[1] >= -cost[1] and ress[2] >= -cost[2]:
        ress = across.addplayerress(session["player"]["pseudo"], session["selected"], cost)
        across.addvaisseau(session["player"]["pseudo"], session["selected"], vinf[0], nb)
    return redirect("/jeu")


@app.route("/updatedata", methods=['POST', 'GET'])
def updatedata():
    session['selected'] = request.form['pla']
    return redirect("/jeu")


@app.route("/jeu",  methods=['POST', 'GET'])
def jeu():
    full = ""

    session["bat"] = across.getbats(session["player"]["pseudo"],
                                    session["selected"])
    planetlist = across.getplanetslist(session["player"]["pseudo"])
    session["ress"] = ("*","*","*")

    vaisseaux = across.getvaisposs(session["player"]["pseudo"],
                                   session['selected'])
    hang = across.gethang(session["player"]["pseudo"],
                                   session['selected'])
    for k,v in planetlist.items():
        if str(k) == session['selected']:
            session["ress"] = v

        tmp = f'''
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
        full += tmp

    return render_template("jeu.html",
                           listpla=full,
                           ress=session["ress"],
                           pname=session['selected'],
                           bat=session["bat"],
                           vaisseaux=vaisseaux,
                           hang=hang)

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
        session["player"]["pseudo"] = "Lenitra"
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
