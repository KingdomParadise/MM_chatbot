import re,requests 

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
            if  response.json()['status']=='OK':
                zipcode=keyword
                print(response.json()['results'][0]['address_components'][1]['short_name'])
                print(response.json()['results'][0]['address_components'][2]['short_name'])
                data = {
                    'ResidenceZip': keyword,
                    'ResidenceCity':response.json()['results'][0]['address_components'][1]['short_name'],
                    'ResidenceState':response.json()['results'][0]['address_components'][2]['short_name'],
                }
                return data 
    else:
        zipcode=None
        return zipcode

def EMAIL_FINDER(message):
    message = str(message).lower()
    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", message)
   
    if len(email)>0 :
        email = email[0]
        response = requests.get("https://isitarealemail.com/api/email/validate",params = {'email': email})
        status = response.json()['status']
        if status=='valid':
            return email
    elif len(email)==0:
        email = None 
        return email
     

 