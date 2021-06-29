import re
from geopy.geocoders import Nominatim

 
 
 
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
            # Using Nominatim Api
            geolocator = Nominatim(user_agent="geoapiExercises") 
            location = geolocator.geocode(keyword) 
            if location is not None:
                print("ZIP_CODE validated by API")
                zipcode=keyword
            else:
                print("FAILDED -- ZIP_CODE validation by API")

        else:
            zipcode=None
    return zipcode
     

 
  
def EMAIL_FINDER(message):
    message = str(message).lower()
    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", message)
   
    if len(email)>0 :
        email = email[0]
    if len(email)==0:
        email = None 
    print(email)
    return email
     

 