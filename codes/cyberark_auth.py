import json
import http.client
import os, datetime, base64, sys, time
from telnetlib import LOGOUT
import ssl
from urllib.request import urlopen

#SERVER VARIABLES
HOST = "comp130.dywoo.local"
PORT = 443

#API URL
LOGONURL = "/PasswordVault/API/Auth/Cyberark/Logon"
LOGOFFURL = "/PasswordVault/API/Auth/Logoff"
testurl= "/PasswordVault/WebServices/auth/Cyberark/CyberArkAuthenticationService.svc/Logoff"
ADDUSERURL = "/PasswordVault/API/Accounts"
UPDATEACCOUNTURL = "/PasswordVault/API/Accounts/{0}"
LINKACCOUNTURL = "/PasswordVault/API/Accounts/{0}/LinkAccount"
VERIFYURL = "/PasswordVault/API/Accounts/{0}/Verify"
RECONCILEURL = "/PasswordVault/API/Accounts/{0}/Reconcile"
CHANGEURL = "/PasswordVault/API/Accounts/{0}/Change"
#Login Detail
USERNAME = 'Administrator' 	#Account used for accessing PVWA webservice
PASSWORD = 	''	#Password for account used for access PVWA webservice

SESSIONID = ''
SESSIONHEADER = ''

#Create HTTPS connection
def createConnection(url, body, header, method):
	logger("Opening connection to server: " + HOST)
	conn = http.client.HTTPSConnection(HOST, PORT, timeout=5, context=ssl._create_unverified_context())
	conn.request(method, url, body, header)
	return conn.getresponse(), conn

#Send API Request
def sendapiRequest(url, body, header, method):
	logger("Sending url request: " + url)
	response, conn = createConnection(url, body, header, method)
	if (response.status >= 300):
		logger(str(response.status) + " - API request failed. Encountered an error. " + response.reason)
		read_res = response.read()
		print(read_res)
		headers = {"content-type":"application/json", 'Authorization' : SESSIONID}
		response, conn = createConnection(LOGOFFURL, "", {"content-type":"application/json", 'Authorization' : SESSIONID}, method)
		if(response.status == 200):
			logger("User [" + USERNAME + "] successsfully logged off")
		conn.close()
		logger("Closed connection. Terminating script...")
		sys.exit()
	else:	
		logger(str(response.status) + " - " + response.reason)
		logger("Closed connection")
		read_res = response.read()
		conn.close()
		if (response.status >= 200):
			if read_res.decode('utf-8')=='':
				data = {}
			else:
				data = json.loads(read_res.decode('utf-8'))
			return data

#Logoff User
def logOffUser():
	logger("Logging out user: " + USERNAME)
	sendapiRequest(LOGOFFURL,"", SESSIONHEADER, "POST")
	logger("Successfully logged out user: " + USERNAME)
	

#Login User
def loginUser():
    os.system("ansible-vault decrypt ~/ansible-automation/vault/pvwa_password --vault-password-file ~/.vault_key")
    with open('/home/dywoo/ansible-automation/vault/pvwa_password') as f:
            contents = f.read()
            contents = ''.join(contents.splitlines())
            PASSWORD = contents
            PASSWORD = PASSWORD
            os.system("ansible-vault encrypt ~/ansible-automation/vault/pvwa_password --vault-password-file ~/.vault_key" )

    logger("Logging in user: " + USERNAME)
    headers = {"content-type":"application/json"}
    body = json.dumps({'username': USERNAME ,'password':PASSWORD, 'concurrentSession': True})
    response = sendapiRequest(LOGONURL, body, headers, "POST")
    #print(response)
    logger("User [" + USERNAME + "] successfully logged in")
    return(response)


#Logger
def logger(msg):
	now = str(datetime.datetime.now())
	print(now + " || " + msg)