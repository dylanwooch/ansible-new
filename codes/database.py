import ipaddress
from operator import rshift
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ansible_vault import Vault
import os


def loginDB():

    vault = Vault(getkey()) #Get Ansible vault key
    creds = vault.load(open('/home/dywoo/ansible-new/vault/vault.yml').read())
    
    #Database Connection URI structure == [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
    url = 'mysql://' + creds['db_user'] + ':' + creds['db_password_py'] + '@' + creds['db_host'] + ':' + creds['db_port'] + '/' + creds['db_database']
    engine = create_engine(url,echo = True)
    return engine

def getkey():
    appdir = os.path.join(os.path.expanduser('~'), '.vault_key')
    with open(appdir) as f:
        key = f.read()
        return key

#Get all instanceId from all pending accounts
def getPending(ipaddress):
    my_conn = loginDB()
    rs = my_conn.execute("SELECT DISTINCT instanceId FROM pendingaccounts WHERE status='pending' and address=%s", ipaddress)
    my_data = rs.fetchall() # a list 
    my_conn.dispose()
    return my_data

#Get CyberArkID if have same Instance ID
# def getID(instance):
#     my_conn = loginDB()
#     rs = my_conn.execute("SELECT id FROM pendingaccounts WHERE instanceId=%s", instance)
#     my_data = rs.fetchall() # a list 
#     my_conn.dispose()
#     return my_data

#Get CyberArk ID if status is 'pending', instanceID and IP Address == automation values
def getID(ipaddress, instance):
    my_conn = loginDB()
    rs = my_conn.execute("SELECT id FROM pendingaccounts WHERE status='pending' and address=%s and instanceId=%s ", ipaddress, instance)
    my_data = rs.fetchall() # a list 
    my_conn.dispose()
    return my_data    

#Get No. of Tries from CyberArkID
def getTries(id):
    my_conn = loginDB()
    rs = my_conn.execute("SELECT noOfTries FROM pendingaccounts WHERE id=%s", id)
    my_data = rs.fetchall() # a list
    my_conn.dispose()
    return my_data

#Get roles (admin,logon or user)
def getRoles(id):
    my_conn = loginDB()
    rs = my_conn.execute("SELECT roles FROM pendingaccounts WHERE id =%s", id)
    my_data = rs.fetchall() # a list 
    my_conn.dispose()
    return my_data

#Update status from 'pending' to 'success'
def updateStatus(id):
    my_conn = loginDB().connect()
    rs = my_conn.execute("UPDATE pendingaccounts SET status = 'success' WHERE id=%s", id)
    return rs

#Update tries by 1
def updateTries(id):
    my_conn = loginDB()
    rs = my_conn.execute("UPDATE pendingaccounts SET noOfTries = noOfTries + 1 WHERE id=%s", id)
    return rs
