import os, pyodbc
from django.conf import settings
import traceback

def generateConnection():
    # conn = pyodbc.connect("DSN=RDTNonprodDatabrick_DSN", autocommit=True)
    conn = pyodbc.connect("Driver={};".format(settings.ADB_DRIVER) +
                      "HOST={};".format(settings.ADB_HOST) +
                      "PORT=443;" +
                      "Schema=default;" +
                      "SparkServerType=3;" +
                      "AuthMech=3;" +
                      "UID=token;" +
                      "PWD={};".format(settings.ADB_TOKEN) +
                      "ThriftTransport=2;" +
                      "SSL=1;" +
                      "HTTPPath={}".format(settings.ADB_HTTP_PATH),
                      autocommit=True)
    print("ADB_Driver={};".format(settings.ADB_DRIVER))
    print("ADB_HOST={};".format(settings.ADB_HOST))
    print("ADB_TOKEN={};".format(settings.ADB_TOKEN))
    print("ADB_HTTPPath={}".format(settings.ADB_HTTP_PATH))
    testConnectADB(conn)
    # print(settings.DRIVER)
    return conn

def testConnectADB(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1")
        for row in cursor.fetchall():
            print(row)
    except:
        raise Exception("Somethings")