from operator import rshift
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ansible_vault import Vault
import os

def loginDB():
    vault = Vault(getkey()) #Get Ansible vault key
    creds = vault.load(open('vault/db_creds.yml').read())
    
    #Database Connection URI structure == [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
    url = 'mysql://' + creds['user'] + ':' + creds['passwd'] + '@' + creds['host'] + ':' + creds['port'] + '/testdb'
    engine = create_engine(url,echo = True)
    return engine

def getkey():
    appdir = os.path.join(os.path.expanduser('~'), '.vault_key')
    with open(appdir) as f:
        key = f.read()
        print(key)
        return key

#Get all instanceId from all pending accounts
def getPending():
    my_conn = loginDB()
    rs = my_conn.execute("SELECT DISTINCT instanceId FROM pendingaccounts WHERE status='pending'")
    my_data = rs.fetchall() # a list 
    my_conn.dispose()
    return my_data

#Get ID if have same Instance ID
def getID(instance):
    my_conn = loginDB()
    rs = my_conn.execute("SELECT id FROM pendingaccounts WHERE instanceId=%s", instance)
    my_data = rs.fetchall() # a list 
    my_conn.dispose()
    return my_data

def getTries(id):
    my_conn = loginDB()
    rs = my_conn.execute("SELECT noOfTries FROM pendingaccounts WHERE id=%s", id)
    my_data = rs.fetchall() # a list
    my_conn.dispose()
    return my_data


def getRoles(id):
    my_conn = loginDB()
    rs = my_conn.execute("SELECT roles FROM pendingaccounts WHERE id =%s", id)
    my_data = rs.fetchall() # a list 
    my_conn.dispose()
    return my_data


def updateStatus(id):
    my_conn = loginDB().connect()
    rs = my_conn.execute("UPDATE pendingaccounts SET status = 'success' WHERE id=%s", id)
    return rs

def updateTries(id):
    my_conn = loginDB()
    rs = my_conn.execute("UPDATE pendingaccounts SET noOfTries = noOfTries + 1 WHERE id=%s", id)
    return rs
