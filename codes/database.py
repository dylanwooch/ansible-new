from operator import rshift
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def loginDB():
    engine = create_engine("mysql://root:P%40ssword123@192.168.233.145:3306/testdb")
    return engine

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
