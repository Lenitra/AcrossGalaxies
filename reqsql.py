import mysql.connector
from confi import *


def readsql(req):
    db = mysql.connector.connect(host=sql_host, user=sql_user, passwd=sql_password)
    cursor = db.cursor()
    cursor.execute("USE AcrossGalaxies;")
    cursor.execute(req)
    recup = cursor.fetchall()
    db.close()
    if recup == []:
        return None
    return recup[0][0]

def reqsql(req):
    db = mysql.connector.connect(host=sql_host, user=sql_user, passwd=sql_password)
    cursor = db.cursor()
    cursor.execute("USE AcrossGalaxies;")
    cursor.execute(req)
    db.commit()
    db.close()