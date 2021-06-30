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
    for keyword in message:
        if len(keyword)==5 and str(keyword).isnumeric():
<<<<<<< HEAD
            # Using Nominatim Api
            # Using Nominatim Api
            geolocator = Nominatim(user_agent="geoapiExercises") 
            location = geolocator.geocode(keyword) 
            if location is not None:
=======
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={keyword}&key=AIzaSyAJGToD7umZ-VdfAl95vSnd1AlxVxt9lUI"
            response = requests.get(url).json()['status']
            if response=='OK':
>>>>>>> dc7e1144ab852f32baaad0de4de56cd2227e36b8
                print("ZIP_CODE validated by API")
                zipcode=keyword
                return zipcode 

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
            
            print(email)
            print("\n\nEMAIL validated by API\n\n")
            return email
    elif len(email)==0:
        email = None 
        print("EMAIL -> NONE")
        return email
     

 