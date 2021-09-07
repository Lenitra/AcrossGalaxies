#!/usr/bin/python
# -*- coding: Utf-8 -*-

from datetime import datetime
from os import system
from flask import Flask, render_template, request, redirect, session
import yaml
import across

app = Flask(__name__)
app.secret_key = "ahcestcontulaspas"
app.debug = True


@app.route('/')
def home():
    # affichage
    try:
        print(session["test"])
    except:
        session["test"] = "lol"
    return render_template("test1.html")


@app.route('/test2')
def test():
    # affichage
    try:
        print(session["test"])
    except:
        print("Session test perdue")
    return render_template("test1.html")



if __name__ == '__main__':
    # website_url = 'across-galaxies.fr:80'
    # app.config['SERVER_NAME'] = website_url
    # app.config["SESSION_FILE_DIR"] = ""
    app.run()
