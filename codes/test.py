from cyberark_auth import *
from database import *

#Get instance ID from database
instanceid = getPending()

for x in range(len(instanceid)):

    ec2id = instanceid[x][0]
    #print(ec2id)
    #Get CyberArk ID from database
    cyberarkid = getID(ec2id)
    #print(cyberarkid)

    #Login to CyberArk
    SESSIONID = loginUser() #Store Session ID to global variable
    SESSIONHEADER = {"content-type":"application/json", 'Authorization' : SESSIONID}
    
    for i in range(len(cyberarkid)):
        caid= cyberarkid[i][0]
        
        #Send API to get JSON using CyberArk ID (caid)
        result = sendapiRequest(UPDATEACCOUNTURL.format(caid), "",SESSIONHEADER, "GET")
        
        #declare variable
        id = result['id']
        tries = getTries(id)
        print(len(tries))
        print(tries[0][0])
        updateTries(id)
        print(tries[0][0])


