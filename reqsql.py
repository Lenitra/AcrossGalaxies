import mysql.connector
from confi import *


def retbrut(req):
    db = mysql.connector.connect(host=sql_host, user=sql_user, passwd=sql_password)
    cursor = db.cursor()
    cursor.execute("USE AcrossGalaxies;")
    cursor.execute(req)
    recup = cursor.fetchall()
    db.close()
    try:
        if recup[0] == []:
            return None
    except:
        pass
    return recup


def readsql(req):
    db = mysql.connector.connect(host=sql_host, user=sql_user, passwd=sql_password)
    cursor = db.cursor()
    cursor.execute("USE AcrossGalaxies;")
    cursor.execute(req)
    recup = cursor.fetchall()
    db.close()
    if recup == []:
        return None
    return recup[0]

def reqsql(req):
    db = mysql.connector.connect(host=sql_host, user=sql_user, passwd=sql_password)
    cursor = db.cursor()
    cursor.execute("USE AcrossGalaxies;")
    cursor.execute(req)
    db.commit()
    db.close()

