import requests
check_avaliability_url = 'https://lifeline.cgmllc.net/api/v2/checkavailability'
user_confituration_url = 'https://lifeline.cgmllc.net/api/v2/userconfiguration'
state_configuration_url = 'https://lifeline.cgmllc.net/api/v2/stateconfiguration'
start_order_url = 'https://lifeline.cgmllc.net/api/v2/startorder'
validate_name_address = ' https://lifeline.cgmllc.net/api/v2/validatenameaddress'
check_duplicate_customer ='https://lifeline.cgmllc.net/api/v2/checkduplicatecustomer'
coverage_check =  'https://lifeline.cgmllc.net/api/v2/coveragecheck'
confirm_state = 'https://lifeline.cgmllc.net/api/v2/confirmstateeligibility'
life_plans_url = 'https://lifeline.cgmllc.net/api/v2/lifelineplans'
submit_order_url = ' https://lifeline.cgmllc.net/api/v2/submitorder'
token='d3a1b634-90a7-eb11-a963-005056a96ce9'
zipcode = 30134
email = 'dene1288@gmail.com'
#state configuration
#res = requests.post(state_configuration_url,data={'Token':token,'state':'GA'}).json()
#print(res['EligibiltyPrograms'][0]['Code'])
#startorder
data = {
        'Token':token,
        'State':'GA',
        'AppVersion':'89.0.4389.72',
        'Platform':'WebApp',
        'SerialNumber':'www.zapier.com',
        'SaleTypeid':3
        }
#res = requests.post(start_order_url,data=data).json()
#print(res)
#validatenameAddress
data = {   #
        'FirstName': 'Test',
        'LastName': 'User',
        'MiddleName':'Middle',
        'DateOfBirth': '01-01-2000',
        'SocialSecurityNo': '1234',
        'StateEligibilityCode': 'GAMCAID',
        'ResidenceAddress01': 'MOSSY VIEW DRIVE',
        'ResidenceCity': 'Douglasville',
        'ResidenceState': 'GA',
        'ResidenceZip': '30134',
        'PackageID': '6a3d8da1-67e6-eb11-a967-005056a9d342',
        'Token': 'd3a1b634-90a7-eb11-a963-005056a96ce9',
        'VendorCode' : 'QUAL',
        'ClientCode' : 'IWI',
        'UserCode' : 'MazamaProdIWI',
        }
data4 = {
"Token": "eb344edb-a833-48e6-b3b7-30eaed05d037",
"PackageID": "eb344edb-a833-48e6-b3b7-30eaed05d037",
"FirstName": "Test",
"MiddleName": "Middle",
"LastName": "User",
"SecondLastName": "Lopez",
"NameSuffix": "I",
"DateOfBirth": "01-01-1950",
"SocialSecurityNo": "1234",
"StateEligibilityCode": "GAMCAID",
"ResidenceAddress01": "101 Vickery St",
"ResidenceCity": "Roswell",
"ResidenceState": "GA",
"ResidenceZip": "30075",
}
#res = requests.post(validate_name_address,data=data).json()
#print(res)
#checkDuplication
data1 = {
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
#res = requests.post(check_duplicate_customer,data=data1).json()
#print(res)

#coverage_check
data2 = {
        "Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
        "PackageID": "6a3d8da1-67e6-eb11-a967-005056a9d342",
        "Tribal": False,
        #"ProgramCode": "LIHEAP",
        "ResidenceAddress01": "MOSSY VIEW DRIVE",
        #"ResidenceAddress02": "",
        "ResidenceCity": "Douglasville",
        "ResidenceState": "GA",
        "ResidenceZip": "30134"
}
#res = requests.post(coverage_check,data=data2).json()

#print(res)
#confirmstate
data3 = {
"Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
"PackageID": "e1fc49de-e1ea-eb11-a967-005056a9d342",
"FirstName": "John",
"LastName": "Smith",
"DateOfBirth": "01-01-1950",
"SocialSecurityNo": "1234",
"ResidenceAddress01": "101 Vickery St",
"ResidenceCity": "Rosewell",
"ResidenceState": "GA",
"ResidenceZip": "30075",
"TribalResident": False,
"Program": "SSI",
}

#res = requests.post("https://lifeline-preprod.cgmllc.net/api/v2/confirmstateeligibility",data=data3).json()

#print(res)

#url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zipcode}&key=AIzaSyAJGToD7umZ-VdfAl95vSnd1AlxVxt9lUI"
#response = requests.get(url)
#print(response.json())
#print(response.json()['results'][0]['address_components'][1]['short_name'])
#print("------------------------")
#print(response.json()['results'][0]['address_components'][2]['short_name'])
data = {
        "Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
        "PackageID": "7fee42f6-81dd-e611-9ed7-005056a97041",
        "State" : "GA",
        "Zip":"30134",

}
res = requests.post(life_plans_url,data=data).json()

plan = []
for i in range(0,len(res['LifelinePlans'])-1):
  mid = ""
  for key in res['LifelinePlans'][i].keys():
      mid+=(key+"-->"+str(res['LifelinePlans'][i][key])+" : ")
  plan.append(mid)   
#print(plan[0])  
Check_NladEbbApplication_Status_url = "https://lifeline.cgmllc.net/api/v2/CheckNVApplicationstatus"
data = {
        "Token":"d3a1b634-90a7-eb11-a963-005056a96ce9",
        "PackageID": "c7ce35c5-3cf1-eb11-a965-005056a96ce9",
        "SSN": "1231",
        "FirstName": "Text",
        "LastName": "User",
        "DOB": "07-17-2001",
        "PrimaryAddress1": "MOSSY VIEW DRIVE",
        "PrimaryCity": "Douglasville",
        "PrimaryState": "GA",
        "PrimaryZip": "30134",
        #"PhoneType": "Wireless",
        #"TribalID": None,
        #"PhoneNumber": None,
        #"UrbanizationCode": None,
        "Tribal": False
}
#res = requests.post(Check_NladEbbApplication_Status_url,data = data).json()
#print(res)

payload = {  # Form request data
        "Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
        "PackageId": "dd130716-64dd-e611-9ed7-005056a97041",
        "EligibilityProgram": "SCSNAP",
        "ResidenceState": "GA",
        "TribalResident": True,
        #"UserSignatureAvailable": True,
        #"PortFreezeOverride": False,
       # "ForceIehForm": False,
        #"Recertification": False,
        #"InvalidAddress": True
    }

#response = requests.post("https://lifeline.cgmllc.net/api/v2/disclosuresconfiguration",headers={"Content-Type": "application/x-www-form-urlencoded"},data=payload)
#print(response.json()['DisclosureItems'])
#print(str(response.json()['CaptureIehForm']))
data = {
"Token":"d3a1b634-90a7-eb11-a963-005056a96ce9",
"PackageID": "c7ce35c5-3cf1-eb11-a965-005056a96ce9",
"EligibilityProgram": "135P",
"FirstName": "John",
"MiddleName": "Norman",
"LastName": "Doe",
#"SecondLastName": "Second",
#"NameSuffix": "Jr",
"DateOfBirth": "1985-09-23",
"Ssn": "4567",
"ResidenceAddress01": "Main Str 101",
"ResidenceAddress02": "Apt 66",
"ResidenceCity": "Rosewell",
"ResidenceState": "AZ",
"ResidenceZip": "30134",
"BestWayToReachYou": "mail",

}

#res = requests.post(submit_order_url,data = data).json()
#print(res)
#Check_NVEligibility_url = "https://lifeline.cgmllc.net/api/v2/checknveligibility"
data = {
        'Token':"d3a1b634-90a7-eb11-a963-005056a96ce9",
        'PackageID': "c7ce35c5-3cf1-eb11-a965-005056a96ce9",
}
#res = requests.post(Check_NVEligibility_url,data = data).json()
#print(res)
get_lifeline_url = "http://lifeline.cgmllc.net/api/v2/getlifelineform"
data = {
        'Token':"d3a1b634-90a7-eb11-a963-005056a96ce9",
        'PackageID': "c7ce35c5-3cf1-eb11-a965-005056a96ce9",
}
res = requests.post(get_lifeline_url,data = data).json()
print(res['Status']) 