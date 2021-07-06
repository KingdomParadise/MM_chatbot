import re, requests 

def INIT_MESSAGE_HANDLER(message):
    message = str(message).lower()
    possible_keywords = ['hello','hola','hi','hey','helo']
    for keyword in possible_keywords:
        if keyword in message:
            init =  'inithello'
            return init
    else: 
        init =  'irrelevent-int--force-zipcode'
        return init

def ZIPCODE_FINDER(message):
    message = str(message).lower().split(' ')
    zipcode=''
    for keyword in message:  
        if len(keyword)==5 and str(keyword).isnumeric():
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={keyword}&key=AIzaSyAJGToD7umZ-VdfAl95vSnd1AlxVxt9lUI"
            response = requests.get(url)
            print(response)
            response = response.json()['status']
            if response=='OK':
                print("ZIP_CODE validated by API")
                zipcode=keyword
                print("-->> zipcode",zipcode)
                return zipcode 

     
def EMAIL_FINDER(message):
    message = str(message).lower()
    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", message)
   
    if len(email)>0 :
        email = email[0]
        response = requests.get("https://isitarealemail.com/api/email/validate",params = {'email': email})
        status = response.json()['status']
        if status=='valid':
            print(response.json())
            print(email)
            print("\n\nEMAIL validated by API\n\n")
            return email
    elif len(email)==0:
        email = None 
        print("EMAIL -> NONE")
        return email
     

def USER_CONFIGURATION_FINDER(token):
        url = 'https://lifeline.cgmllc.net/api/v2/userconfiguration'
        #myobj = {'Token': token}
        myobj = {'Token': 'd3a1b634-90a7-eb11-a963-005056a96ce9'}
  
        response = requests.get(url,params=myobj)
        print(response)
        if response.json()['Response']['Status']=="Success":
            return response.json()['Response']
        else:
            return ""
        
def START_ORDERATION(token,SerialNumber,Platform,AppVersion,State,StaleTypeld,Latitude,Longitude):
    url = 'http://lifeline.cgmllc.net/api/v2/startorder'
    myobj = {'Token': token, 
             'SerialNumber' : SerialNumber, 
             'Platform': Platform,
             'AppVersion': AppVersion,
             'State': State,
             'StaleTypeld': StaleTypeld,
             'Latitude': Latitude,
             'Longitude': Longitude
             }
    myobj_Test = {'Token': ' ', 
             'SerialNumber' : 'www.zapier.com', 
             'Platform': 'WebApp',
             'AppVersion': '89.0.4389.72',
             'State': '',
             'StaleTypeld': '3',
             'Latitude': '',
             'Longitude': ''
             }
    response = requests.get(url,params=myobj_Test)
    print(response)
    if response.json()['Response']['Status']=="Success":
            return response.json()['Response']
    else:
            return ""
     