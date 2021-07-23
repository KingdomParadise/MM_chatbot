import requests
check_avaliability_url = 'https://lifeline.cgmllc.net/api/v2/checkavailability'
user_confituration_url = 'https://lifeline.cgmllc.net/api/v2/userconfiguration'
state_configuration_url = 'https://lifeline.cgmllc.net/api/v2/stateconfiguration'
start_order_url = 'https://lifeline.cgmllc.net/api/v2/startorder'
validate_name_address = ' https://lifeline.cgmllc.net/api/v2/validatenameaddress'
check_duplicate_customer ='https://lifeline.cgmllc.net/api/v2/checkduplicatecustomer'
coverage_check =  'https://lifeline.cgmllc.net/api/v2/coveragecheck'
confirm_state = 'https://lifeline.cgmllc.net/api/v2/confirmstateeligibility '

token='d3a1b634-90a7-eb11-a963-005056a96ce9'

import time,os,uuid,json,re,sched, timeit,django  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()
from root.models import ChatTracker

def CheckAvailability_API(zipcode,email):
    print('-->> Calling CheckAvailability_API')
    res = requests.post(check_avaliability_url, data={'Token':token,'ZipCode':zipcode,'Email':email}).json()
    if res['Status']=='Success':
        return 1
    else:  
        return None

def UserConfiguration_API():
    print('-->> Calling UserConfiguration_API')
    res = requests.post(user_confituration_url,data={'Token':token}).json()
    if res['Status']=='Success':
        data = {
            'ReservationUserCode' : res['ReservationUserCode'],
            'ReservationAgentCode' : res['ReservationAgentCode'],
            'ReservationClientCode' : res['ReservationClientCode'],
            'ReservationVendorCode' : res['ReservationVendorCode'],
        }
        return data
    else:
        return None

def StateConfiguration_API(id):
    print('-->> Calling StateConfiguration_API')
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    print("ResidenceState-->" + str(currentchat.ResidenceState))

    res = requests.post(state_configuration_url,data={'Token':token,'state':currentchat.ResidenceState}).json()
    print(res['EligibiltyPrograms'][0]['Code'])
    if res['Status']=='Success':
        if currentchat.ResidenceState == "CA":
            data = {
                'TribalEligible' : res['TribalEligible'],
                'FcraDisclosureText' : res['FcraDisclosureText'],
                'FcraAdditionalDisclosureText' : res['FcraAdditionalDisclosureText'],
                'FcraAcknowledgement' : res['FcraAcknowledgement'],
                'EligibiltyPrograms' : res['EligibiltyPrograms'][0]['Code']
            }
            return data
        else:
            data = {
                'TribalEligible' : res['TribalEligible'],
                'EligibiltyPrograms' : res['EligibiltyPrograms'][0]['Code']
            }
            return data
    else:
        return None

def StartOrder_API(id):
    print('-->> Calling StartOrder_API')
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    print("ResidenceState-->" + str(currentchat.ResidenceState))

    data = {
        'Token':token,
        'State':currentchat.ResidenceState,
        'AppVersion':'89.0.4389.72',
        'Platform':'WebApp',
        'SerialNumber':'www.zapier.com',
        'SaleTypeid':3
        }
    res = requests.post(start_order_url,data=data).json()
    
    if res['Status']=='Success':
        data = {
                'OrderNumber' : res['OrderNumber'],
                'PackageId' : res['PackageId'],
            }
        return data
    else:
        return None

def CheckDuplicateCustomer():
    print('-->>Calling CheckDuplicateCustomer')
    data = {
        "Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
        "PackageID": "6a3d8da1-67e6-eb11-a967-005056a9d342",
        "FirstName": "John",
        #"MiddleName": "Middle",
        "LastName": "Smith",
        #"SecondLastName": "Smith",
        "DateOfBirth": "1995-02-05",
        "Ssn": "1234",
        "ResidenceAddress01": "101 Vickery St",
        "ResidenceCity": "Roswell",
        "ResidenceState": "GA",
        "ResidenceZip": "30075"
    }

def FLOWCHART3(zipcode,email,chatid):
    currentchats = ChatTracker.objects.filter(chatid=chatid)
    currentchat = currentchats.first()
    check = CheckAvailability_API(zipcode,email)
    if check:
        userConfiguration = UserConfiguration_API()
        if userConfiguration:
            stateConfiguration = StateConfiguration_API(chatid)
            if stateConfiguration:
                startOrder = StartOrder_API(chatid)
                if startOrder:
                    if currentchat.ResidenceState =="CA":
                        data = {
                            'ReservationUserCode' : userConfiguration['ReservationUserCode'],
                            'ReservationAgentCode' : userConfiguration['ReservationAgentCode'],
                            'ReservationClientCode' : userConfiguration['ReservationClientCode'],
                            'ReservationVendorCode' : userConfiguration['ReservationVendorCode'],

                            'TribalEligible' : stateConfiguration['TribalEligible'],
                            'FcraDisclosureText' : stateConfiguration['FcraDisclosureText'],
                            'FcraAdditionalDisclosureText' : stateConfiguration['FcraAdditionalDisclosureText'],
                            'FcraAcknowledgement' : stateConfiguration['FcraAcknowledgement'],
                            'EligibiltyPrograms' : stateConfiguration['EligibiltyPrograms'],


                            'OrderNumber' : startOrder['OrderNumber'],
                            'PackageId' : startOrder['PackageId'],
                        }
                        print('==>>>>  All API Layers PASSED')
                        return data
                    else:  
                        data = {
                            'ReservationUserCode' : userConfiguration['ReservationUserCode'],
                            'ReservationAgentCode' : userConfiguration['ReservationAgentCode'],
                            'ReservationClientCode' : userConfiguration['ReservationClientCode'],
                            'ReservationVendorCode' : userConfiguration['ReservationVendorCode'],

                            'TribalEligible' : stateConfiguration['TribalEligible'],
                            'EligibiltyPrograms' : stateConfiguration['EligibiltyPrograms'],

                            'OrderNumber' : startOrder['OrderNumber'],
                            'PackageId' : startOrder['PackageId'],
                        }
                        print('==>>>>  All API Layers PASSED')
                        return data  
                else:
                    print('** API_1 FAILED :(')
                    return 'error_at_api4'
            else:
                print('** API_1 FAILED :(')
                return 'error_at_api3'
        else:
            print('** API_1 FAILED :(')
            return 'error_at_api2'
    else:
        print('** API_1 FAILED :(')
        return 'error_at_api1'

#FlowChart 4        
def NationalVerification(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    #data = {
       
      #  'FirstName': items.first_name,
     #   'LastName': items.last_name,
      #  'MiddleName':items.middle_name,
      #  'DateOfBirth': items.date,
      #  'SocialSecurityNo': items.last_four_social,
      #  'StateEligibilityCode': 'GAMCAID',
      #  'SecondLastName': items.second_last_name,
      #  'NameSuffix': items.suffix,
      # 'ResidenceAddress01': items.residential_address,
      #  'ResidenceCity': 'Roswell',
      #  'ResidenceState': 'GA',
      #  'ResidenceZip': '30075',
      #  'HasPackageId' : True,
      #  'PackageID': '6a3d8da1-67e6-eb11-a967-005056a9d342',
      #  'Token': 'd3a1b634-90a7-eb11-a963-005056a96ce9',

       # }
    print(currentchat.date)
    data = {
        'FirstName': currentchat.first_name,
        'LastName': currentchat.last_name,
        'DateOfBirth': currentchat.date,
        'SocialSecurityNo': currentchat.last_four_social,
        'StateEligibilityCode': currentchat.EligibiltyPrograms,
        'ResidenceAddress01': currentchat.residential_address,
        'ResidenceCity': currentchat.ResidenceCity,
        'ResidenceState': currentchat.ResidenceState,
        'ResidenceZip': currentchat.ResidenceZip,
        'PackageID': currentchat.PackageId,
        'Token': 'd3a1b634-90a7-eb11-a963-005056a96ce9',
        'VendorCode' : currentchat.ReservationVendorCode,
        'ClientCode' : currentchat.ReservationClientCode,
        'UserCode' : currentchat.ReservationUserCode,
        }
    print(currentchat.EligibiltyPrograms)
    res = requests.post(validate_name_address,data=data).json()
    return  res  
#Flowchat5
def Check_dulicate_customer(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {   
        "Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
        #"PackageID": "6a3d8da1-67e6-eb11-a967-005056a9d342",
        "PackageID": currentchat.PackageId,
 #       "FirstName": "John",
        "FirstName": currentchat.first_name,
 #       "LastName": "Smith",
        "LastName": currentchat.last_name,
 #       "DateOfBirth": "1995-02-05",
        "DateOfBirth": currentchat.date,
  #      "Ssn": "1234",
        "Ssn": currentchat.last_four_social,
 #       "ResidenceAddress01": "101 Vickery St",
        "ResidenceAddress01": currentchat.residential_address,
        "ResidenceCity": currentchat.ResidenceCity,
        "ResidenceState": currentchat.ResidenceState,
        "ResidenceZip": currentchat.ResidenceZip
    }   
    res = requests.post(check_duplicate_customer,data=data).json()
    if res['Status'] == "Success":
        return res
    else:
        return None    
def Coverage_check(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {
        "Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
 #       "PackageID": "6a3d8da1-67e6-eb11-a967-005056a9d342",
         "PackageID": currentchat.PackageId,
 #       "Tribal": False,
        "Tribal": currentchat.TribalResident,
#        "ProgramCode": "LIHEAP",
 #       "ResidenceAddress01": "101 Vickery St",
        "ResidenceAddress01": currentchat.residential_address,
 #       "ResidenceAddress02": "",
        "ResidenceCity": currentchat.ResidenceCity,
        "ResidenceState": currentchat.ResidenceState,
        "ResidenceZip": currentchat.ResidenceZip
        }
    res = requests.post(coverage_check,data=data).json()
    #if res['TribalFail'] == True or res['TribalMismatch'] == True or res['TribalProgramMismatch'] ==True:
    #    currentchat.TribalResident = False
    #if    res['TribalFail'] == False and res['TribalMismatch'] == False and res['TribalProgramMismatch'] ==False and res['TribalVerified'] ==True:
    #    currentchat.TribalResident = False
    if res['Status'] == "Success":
        return res
    else:
        return None   

def ConfirmState(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data3 = {
        "Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
        #"PackageID": "e1fc49de-e1ea-eb11-a967-005056a9d342",
        "PackageID": currentchat.PackageId,
        #"FirstName": "John",
        "FirstName": currentchat.first_name,
        #"LastName": "Smith",
        "LastName":currentchat.last_name,
        #"DateOfBirth": "02-05-1995",
        "DateOfBirth":currentchat.date,
        #"SocialSecurityNo": "1234",
        "SocialsecurityNo":currentchat.last_four_social,
        #"ResidenceAddress01": "101 Vickery St",
        "ResidenceAddress01": currentchat.residential_address,
        "ResidenceCity": currentchat.ResidenceCity,
        "ResidenceState": currentchat.ResidenceState,
        "ResidenceZip": currentchat.ResidenceZip,
        #"TribalResident": False,
        "TribalResident":currentchat.TribalResident,
        #"Program": "SSI",
        "Program":currentchat.program
    }
    res = requests.post(confirm_state,data=data3).json()
    if res['Status'] == "Success":
        return res
    else:
        return None    

def FLOWCHAT5(id):
    if Check_dulicate_customer(id):
        response = Coverage_check(id)
        if response:
            if response['Coverage'] == True:
                reply = "Pass"
                return reply
            else:
                reply = "No-Pass"  
                return reply  
    reply = "error"    
    return reply

if __name__ == '__main__':
    email='denea1288@gmail.com'
    email='denea128822@gmail.com'
    zipcode=30314
    #print(FLOWCHART3(zipcode,email))