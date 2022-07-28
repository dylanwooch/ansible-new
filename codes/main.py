from cyberark_auth import *
from database import *



#Get instance ID from database
instanceid = getPending()

for x in range(len(instanceid)):

    ec2id = instanceid[x][0]
    
    #Get CyberArk ID from database
    cyberarkid = getID(ec2id)

   
    
    for i in range(len(cyberarkid)):
        caid= cyberarkid[i][0]
        
        #Login to CyberArk
        SESSIONID = loginUser() #Store Session ID to global variable
        SESSIONHEADER = {"content-type":"application/json", 'Authorization' : SESSIONID}

        #Send API to get JSON using CyberArk ID (caid)
        result = sendapiRequest(UPDATEACCOUNTURL.format(caid), "",SESSIONHEADER, "GET")
        

        while not isSuccess and tries[0][0] < 5:
            #declare variable
            id = result['id']
            role = getRoles(id)
            tries = getTries(id)
            isSuccess = False
            
            if "status" in result['secretManagement']:
                if result['secretManagement']['status'] == "success":
                    updateStatus(id)
                    updateTries(id)
                    isSuccess = True
                    logger(id + " successfully updated ")
                    break
                elif result['secretManagement']['status'] == "failure":
                    if role == "admin" or "logon":
                        sendapiRequest(CHANGEURL.format(id),"",SESSIONHEADER, "POST")
                        updateTries(id)
                    elif role == "user":
                        sendapiRequest(RECONCILEURL.format(id),"",SESSIONHEADER, "POST")
                        updateTries(id)
                print(f"tries {tries[0][0]}")
            else:
                ("Please wait for account status")
                time.sleep(60)

                #Send API to get JSON using CyberArk ID (caid)
                result = sendapiRequest(UPDATEACCOUNTURL.format(caid), "",SESSIONHEADER, "GET")



        
        




#Logoff
# sendapiRequest(LOGOFFURL,"", SESSIONHEADER, "POST")
# logger("Successfully logged out user: " + USERNAME)


