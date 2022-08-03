from cyberark_auth import *
from database import *



#Get instance ID from database
instanceid = getPending()

for x in range(len(instanceid)):

    ec2id = instanceid[x][0]
    print(ec2id)
    #Get CyberArk ID from database
    cyberarkid = getID(ec2id)
    print(cyberarkid)

    #Login to CyberArk
    SESSIONID = loginUser() #Store Session ID to global variable
    SESSIONHEADER = {"content-type":"application/json", 'Authorization' : SESSIONID}
    

    #trigger login once
    #loop through login user

    #trigger admin once
    #loop through admin user


    #trigger all functional accounts once
    #loop through the status of each user

    for i in range(len(cyberarkid)):
        caid= cyberarkid[i][0]
        
        #Send API to get JSON using CyberArk ID (caid)
        result = sendapiRequest(UPDATEACCOUNTURL.format(caid), "",SESSIONHEADER, "GET")
        print(result)

        #declare variable
        id = result['id']
        tries = getTries(id)
        isSuccess = False
        logger("Going in while loop")

        while not isSuccess and (tries[0][0]) < 5:   
            if "status" in result['secretManagement']:
                if result['secretManagement']['status'] == "success":
                    updateStatus(id)
                    updateTries(id)
                    isSuccess = True
                    logger(id + " successfully updated ")
                    break
                elif result['secretManagement']['status'] == "failure":
                    role = getRoles(id)
                    if role == "admin" or "logon":
                        sendapiRequest(CHANGEURL.format(id),"",SESSIONHEADER, "POST")
                        updateTries(id)

                    elif role == "user":
                        sendapiRequest(RECONCILEURL.format(id),"",SESSIONHEADER, "POST")
                        updateTries(id)
                
                #update result after sending API 
                result = sendapiRequest(UPDATEACCOUNTURL.format(caid), "",SESSIONHEADER, "GET")
            else:
                print("Please wait for account status")
                time.sleep(60)

                #keep checking APIs
                result = sendapiRequest(UPDATEACCOUNTURL.format(caid), "",SESSIONHEADER, "GET")



        
        




#Logoff
# sendapiRequest(LOGOFFURL,"", SESSIONHEADER, "POST")
# logger("Successfully logged out user: " + USERNAME)


