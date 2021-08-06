#!/usr/bin/python
# -*- coding: Utf-8 -*-

from datetime import datetime
from threading import Semaphore
from flask import Flask, render_template, request, redirect, session
import socket

app = Flask(__name__)
app.secret_key = "ahcestcontulaspas"
app.debug = True


@app.route('/')
def home():
    # affichage du html
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Session est une variable qui est stocké dans le serveur et qui est propre à chaque utilisateur
    session["player"] = {"pseudo": "", "mail": ""}
    return render_template("logreg.html")


if __name__ == '__main__':
    app.run(host=socket.gethostname(), port=8080)
