import re,requests 
from root.models import ChatTracker
from CSGM_APIs import FLOWCHAT5,ConfirmState, NationalVerification
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
def get_start(chatid, init_message):
    avaliable_choices = ['inithello','irrelevent-int--force-zipcode','zipcode','email']
    currentchats = ChatTracker.objects.filter(chatid=chatid)
    currentchat = currentchats.first()

    if init_message in avaliable_choices:
        currentchat.init_message = init_message
        currentchat.save() 
        reply = ["Hello!👋 I am a bot and I am here to help. What is your Zip Code?","normal"]
        return reply  
    else:
        reply = ["Hello!👋 I am a bot and I am here to help. What is your Zip Code?","normal"]
        return reply 
def ZIPCODE_FINDER(chatid,message):
    currentchats = ChatTracker.objects.filter(chatid=chatid)
    currentchat = currentchats.first()

    message = str(message).lower().split(' ')
    zipcode=''
    for keyword in message:  
        if len(keyword)==5 and str(keyword).isnumeric():
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={keyword}&key=AIzaSyAJGToD7umZ-VdfAl95vSnd1AlxVxt9lUI"
            response = requests.get(url)
            if  response.json()['status']=='OK':
                zipcode=keyword
                currentchat.ResidenceZip = zipcode
                currentchat.ResidenceCity = response.json()['results'][0]['address_components'][1]['short_name']
                currentchat.ResidenceState = response.json()['results'][0]['address_components'][2]['short_name']
                currentchat.save()
                return ["Great! That was a valid zip code! 🎉\nPlease enter your email address? (Ex: example@mail.com) 💬","normanl"]
    else:
        return  ["That Zip Code was not valid. Please enter a valid zip code.","normal"]

def EMAIL_FINDER(chatid,message):
    currentchats = ChatTracker.objects.filter(chatid=chatid)
    currentchat = currentchats.first()

    message = str(message).lower()
    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", message)
   
    if len(email)>0 :
        email = email[0]
        response = requests.get("https://isitarealemail.com/api/email/validate",params = {'email': email})
        status = response.json()['status']
        if status=='valid':
            currentchat.email = email
            currentchat.save()
            currentchat.init_message = "STARTFLOWCHART3"
            currentchat.save()
            return ["Thank You! This will just take a few seconds You are on your way to a FREE phone!📱","normal_autoPass"]
    elif len(email)==0:
        return  ["That email address was not valid. Please enter a working email address. (Ex: example@mail.com)","normal"]
     
def GET_FLOWCHAT_STATE(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    if 'restart' in incoming_message:
        currentchat.flowchart3_stucked_status = False
        currentchat.save()
        return ['Please enter a valid ZipCode.','normal']
    elif 'help' in incoming_message :
        currentchat.flowchart3_stucked_status = False
        return ['An agent will reach out shortly! Thank you for your patience.','normal']
       
def STARTFLOWCHAT4(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    if currentchat.TribalEligible == True:
        reply = ["Do you reside on Federally-recognized Tribal lands?","normal_yes_no"]
        currentchat.init_message = "TribalResident"   
        currentchat.save()
        return reply
    else:
        currentchat.TribalResident = False
        currentchat.init_message = "Confirm_information"
        reply = ["Confirm your information again?","normal_autoPass"]
        currentchat.save() 
        return reply
def SET_TribalResident(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    if 'yes' in incoming_message:
        currentchat.TribalResident = True
        currentchat.save() 
    elif 'no' in incoming_message:
        currentchat.TribalResident = False
        currentchat.save() 
    currentchat.init_message = "Confirm_information"
    currentchat.save() 
    return ["Confirm your information again?","normal_autoPass"]

def SET_ConfirmInfo(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    currentchat.init_message = "edit"
    currentchat.save()
    return ["Confirm your information again?",currentchat.first_name, currentchat.middle_name, currentchat.last_name,currentchat.suffix,currentchat.date,currentchat.last_four_social,currentchat.residential_address,currentchat.apt_unit1,currentchat.ResidenceCity,currentchat.ResidenceState,currentchat.ResidenceZip]

def EDIT_Info(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    if 'yes' in incoming_message:
        reply = ["What would you like to edit?","FirstName", "MiddleName", "LastName","Suffix","DateOfBirth","Socical Security Number","ResidenceAddress","Apt","ResidenceCity","State","ZipCode"]
        currentchat.init_message = "edit_item"
        currentchat.save()
        return reply
    elif 'no' in incoming_message:
        result = NationalVerification(id)
        if  result['Status'] == "Success":
            if currentchat.ResidenceState!="CA":
                currentchat.init_message = "CGMChecks"
                currentchat.save()
                return ["CGM Checks...","normal_autoPass"]
            else:
                currentchat.init_message = "FCRATEXT"
                currentchat.save()
                return ["FCRADISCLOSURETEXT :"+currentchat.FcraDisclosureText+"  FCRAADDITIONALDISCLOSURETEXT:"+currentchat.FcraAdditionalDisclossureText+"  FCRAACKNOWLEDGEMENT : "+currentchat.FcraAcknowledgement+" - I agree : y/[n","normal"] 
        elif result['Status'] == "Failure":
            currentchat.init_message = "Confirm_information"
            currentchat.save()
            if "Invalid" in result['Message'] :
                return ["Your information did not pass out checks!","normal"]
            elif "Validation error" in result['Message'] :
                return ["Oh no! WE couldn't validate your information."+str(result['ValidationErrors']) +"Please correct the error","normal"]
        else:
            return ["Please Select the one of buttons","normal"] 
            
def EDIT_Info_item(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    currentchat.init_message = "save_item"
    currentchat.variable_state = incoming_message
    currentchat.save()
    return ["Please Enter the "+ incoming_message + " again","normal"]

def SAVE_Info(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    currentchat.init_message = "Confirm_information"
    currentchat.save()
    if currentchat.variable_state == "FirstName":
        currentchat.first_name = incoming_message  
        currentchat.save()
    elif currentchat.variable_state == "MiddleName":
        currentchat.middle_name = incoming_message 
        currentchat.save()
    elif currentchat.variable_state == "LastName":
        currentchat.last_name = incoming_message 
        currentchat.save()
    elif currentchat.variable_state == "Suffix":
        currentchat.suffix = incoming_message 
        currentchat.save()
    elif currentchat.variable_state == "DateOfBirth":
        currentchat.date = incoming_message
        currentchat.save()
    elif currentchat.variable_state == "Socical Security Number":
        if len(incoming_message)==4 and str(incoming_message).isnumeric():
            currentchat.last_four_social = incoming_message
            currentchat.save()
    elif currentchat.variable_state == "ResidenceAddress":
        currentchat.residential_address = incoming_message
        currentchat.save()
    elif currentchat.variable_state == "Apt":
        currentchat.apt_unit1 = incoming_message  
        currentchat.save()
    elif currentchat.variable_state == "ResidenceCity":
        currentchat.ResidenceCity = incoming_message 
        currentchat.save()
    elif currentchat.variable_state == "ZipCode":
        currentchat.ResidenceZip = incoming_message
        currentchat.save()
    elif currentchat.variable_state == "State":
        currentchat.ResidenceState = incoming_message
        currentchat.save()
    currentchat.variable_state = ""
    return["Continue","normal_autoPass"]

def FCRATEXT(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    if "y" in incoming_message:
        currentchat.init_message = "CGMChecks"
        currentchat.save()
        return ["CGM Checks...","normal_autoPass"]    
            
def CGMChecks(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()  
    response = FLOWCHAT5(id)
    if response=="error":
        currentchat.init_message="help"
        currentchat.save()
        return ["Oh no! Our System is having trouble wity your request","normal"]
    elif response=="No-Pass":
        currentchat.init_message = "End_chat"
        currentchat.save()
        return ["Sorry! We do not currently offer coverage in your area.","normal"]
    elif response == "Pass":
        if currentchat.ResidenceState!="CA":
            currentchat.init_message = "Lifeline"
            currentchat.save()
            return ["Let's start Lisfeline",'normal']
        elif ConfirmState(id):
            currentchat.init_message = "Lifeline"
            currentchat.save()
            return ["Let's start Lisfeline",'normal']
        else:
            currentchat.init_message = "ConfirmError"
            currentchat.save()
            return ["Oh no! Our system is having trouble with your request",'normal']
             
