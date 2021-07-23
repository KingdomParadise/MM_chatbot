#from django.db.models.enums import IntegerChoices
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time,os,uuid,json,re,sched, timeit,django  
from analyzer import *
from CSGM_APIs import FLOWCHART3, NationalVerification,FLOWCHAT5,ConfirmState



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from root.models import ChatTracker


chatid = "O4U5YHR1ESL"
message = "Hello, how are u ?"
message = "THIS IS my zip code 40100"
message = "THIS IS my zip code 40100 mashood@gmail.com"


def CLEAR_ENTITY(currentchat):
    currentchat.ResidenceZip=''
    currentchat.email=''
    currentchat.flowchart3_stucked_status=False
    currentchat.save()


def generateReply(chatid,incoming_message): 

    ischatidexist = ChatTracker.objects.filter(chatid=chatid).exists()
    if ischatidexist:pass
    else:ChatTracker(chatid=chatid).save()

    currentchat = ChatTracker.objects.get(chatid=chatid)
    avaliable_choices = ['inithello','irrelevent-int--force-zipcode','zipcode','email']
    print(chatid)
    if currentchat.init_message=='':
        init_message = INIT_MESSAGE_HANDLER(incoming_message) 
        if init_message in avaliable_choices:
            currentchat.init_message = init_message
            currentchat.save() 
            reply = ["Hello!👋 I am a bot and I am here to help.","What is your Zip Code?"]
            return reply  
        else:
            reply = ["Hello!👋 I am a bot and I am here to help.","What is your Zip Code?"]
            return reply  

    elif currentchat.init_message !='':
        if currentchat.ResidenceZip=='':
            # extract ZIP CODE
                data = ZIPCODE_FINDER(incoming_message)
            # extract ZIP CODE
                if data is not None: 
                    currentchat.ResidenceZip = data['ResidenceZip']
                    currentchat.ResidenceCity = data['ResidenceCity']
                    currentchat.ResidenceState = data['ResidenceState']
                    currentchat.save()
                    reply = "Great! That was a valid zip code! 🎉\nPlease enter your email address? (Ex: example@mail.com) 💬"
                    return reply
                elif data==None:
                    reply = "That Zip Code was not valid. Please enter a valid zip code."
                    return reply
        

        elif len(str(currentchat.ResidenceZip))==5 and currentchat.email=='':
            # extract phone number  
            email = EMAIL_FINDER(incoming_message)
            if email is not None:
                currentchat.email = email
                currentchat.save()
                reply = "Thank You! This will just take a few seconds You are on your way to a FREE phone!📱"
                currentchat.init_message = "STARTFLOWCHART3"
                currentchat.save()
                return reply
            elif email is None:
                reply = "That email address was not valid. Please enter a working email address. (Ex: example@mail.com)"
                return reply

        #  HANDLING FLOWCHART 3
        elif currentchat.flowchart3_stucked_status is True:
            incoming_message = incoming_message.lower()
            if 're start' in incoming_message or 're-start' in incoming_message or 'restart' in incoming_message:
                reply = 'Please enter a valid ZipCode.'
                currentchat.flowchart3_stucked_status = False
                currentchat.save()
                CLEAR_ENTITY(currentchat)
                return reply
            elif 'help' in incoming_message :
                reply = 'An agent will reach out shortly! Thank you for your patience.'
                currentchat.flowchart3_stucked_status = False
                return reply
            else:
                print("--> Neither HELP Nor RE-START detected !")
                reply = "Please type Restart to re-enter other valid information OR type Help to talk to our Agent"
                return reply

        elif currentchat.init_message=='STARTFLOWCHART3':
            response = FLOWCHART3(currentchat.ResidenceZip,currentchat.email,currentchat.chatid)
            if response=='error_at_api1':
                reply = f'Sorry! We currently do not offer any service plans for the ZIP CODE {currentchat.ResidenceZip} area. Please try with other ZipCode.'
                CLEAR_ENTITY(currentchat)
                return reply
            elif response=='error_at_api2' or response=='error_at_api3' or response=='error_at_api4' :
                currentchat.flowchart3_stucked_status=True
                currentchat.save()
                reply = "Oh no! Our system is having trouble with your application. : restart/[help]"
                return reply
            else:
                currentchat.init_message = 'ValidSSN'
                currentchat.ReservationUserCode = response['ReservationUserCode']
                currentchat.ReservationAgentCode = response['ReservationAgentCode']
                currentchat.ReservationClientCode = response['ReservationClientCode']
                currentchat.ReservationVendorCode = response['ReservationVendorCode']
                currentchat.TribalEligible = response['TribalEligible']
                currentchat.OrderNumber = response['OrderNumber']
                currentchat.PackageId = response['PackageId']

                if currentchat.ResidenceState  == "CA":
                    currentchat.FcraDisclosureText = response['FcraDisclosureText']
                    currentchat.FcraAdditionalDisclosureText = response['FcraAdditionalDisclosureText']
                    currentchat.FcraAcknowledgement = response['FcraAcknowledgement']

                currentchat.save()
                reply = f'http://localhost:8000/submit_info/{chatid}'
                return reply
        elif currentchat.init_message=="ValidSSN":
             if len(incoming_message)==4 and str(incoming_message).isnumeric():
                currentchat.init_message = "STARTFLOWCHART4"
                currentchat.save()
                reply = "The social security number is entered correctly"
                return reply
             else:
                 reply = "Please enter the correct number - 4 digit numbers"   
                 return reply
        elif currentchat.init_message == 'STARTFLOWCHART4':
            if currentchat.TribalEligible == True:
                reply = "Do you reside on Federally-recognized Tribal lands? : yes/[no]"
                currentchat.init_message = "TribalResident"   
                currentchat.save()
                return reply
            else:
                currentchat.TribalResident = False
                currentchat.init_message = "Confirm_information"
                reply = "Do you confirm your entered information correctly again? : yes/[no]"
                currentchat.save() 
                return reply
        elif currentchat.init_message == "TribalResident":
            if 'yes' in incoming_message:
                currentchat.TribalResident = True
                currentchat.save() 
            elif 'no' in incoming_message:
                currentchat.TribalResident = False
                currentchat.save() 
            else:
                reply = "Please enter : yes/[no]:"
                return reply
            currentchat.init_message = "Confirm_information"
            reply = "Do you confirm your entered information correctly again? : yes/[no]"
            currentchat.save() 
            return reply 

        elif currentchat.init_message == "Confirm_information":   
            if 'yes' in incoming_message:
                currentchat.init_message = "edit"
                currentchat.save()
                reply = "What would you like to edit? : Name/[DOB]/[Social Security]/[Address]"
                return reply
            elif 'no' in incoming_message:
                result = NationalVerification(currentchat.chatid)
                if  result['Status'] == "Success":
                    if currentchat.ResidenceState!="CA":
                        currentchat.init_message = "CGMChecks"
                        currentchat.save()
                        return ("CGM Checks...")
                    else:
                        reply = "FCRADISCLOSURETEXT :"+currentchat.FcraDisclosureText+"  FCRAADDITIONALDISCLOSURETEXT:"+currentchat.FcraAdditionalDisclossureText+"  FCRAACKNOWLEDGEMENT : "+currentchat.FcraAcknowledgement +"  Do you agee?/y:[n]" 
                        currentchat.init_message = "FCRATEXT"
                        currentchat.save()
                        return reply
                elif result['Status'] == "Failure":
                    currentchat.init_message = "edit"
                    currentchat.save()
                    if "Invalid" in result['Message'] :
                        reply = "Your information did not pass out checks!"
                        return reply
                    elif "Validation error" in result['Message'] :
                        reply = "Oh no! WE couldn't validate your information."+str(result['ValidationErrors']) +"Please correct the error"+":Name/[DOB]/[Social Security]/[Address]"
                        return reply
                # else:
                #     reply = "Please enter yes/[no]"
                #     return reply        

        elif currentchat.init_message == "edit":
            if "Name"  in incoming_message   or "DOB" in incoming_message:
                currentchat.init_message = "edit_else"
                currentchat.save()
                reply = f'http://localhost:8000/submit_info/{chatid}'
                return reply
            elif "Address" in incoming_message:
                currentchat.init_message = "edit_else"
                currentchat.save()
                reply = f'http://localhost:8000/submit_info/{chatid}'
                return reply
            elif "Social Security" in incoming_message:
                currentchat.init_message = "edit_else_social"
                currentchat.save()
                reply = "What are the last four digits of your social  security number?What are the last four  digits of your social security number?"
                return reply
            else:
                reply = "Choose item to edit : Name/[DOB]/[Social Security]/[Address]"
                return reply
        elif currentchat.init_message == "edit_else_social":
            #validate the digit number later
             if len(incoming_message)==4 and str(incoming_message).isnumeric():
                currentchat.init_message = "edit_else"
                currentchat.last_four_social = incoming_message
                currentchat.save()
                reply = "The social security number is entered correctly"
                return reply
             else:
                 reply = "Please enter the correct number/ only 4 digit numbers"   
                 return reply
        elif currentchat.init_message == "edit_else":
             reply = "Would you like to edit anything else? : yes/[no]" 
             currentchat.init_message = "edit_else_answer"
             currentchat.save()
             return reply
        elif currentchat.init_message == "edit_else_answer":
            if 'yes' in incoming_message:
                currentchat.init_message = "edit"
                currentchat.save()
                reply = "What would you like to edit"
                return reply       
            elif 'no' in incoming_message:
                result = NationalVerification(currentchat.chatid)
                if  result['Status'] == "Success":
                    if currentchat.ResidenceState!="CA":
                        currentchat.init_message = "CGMChecks"
                        currentchat.save()
                        return ("CGM Checks...")
                    else:
                        reply = "FCRADISCLOSURETEXT :"+currentchat.FcraDisclosureText+"  FCRAADDITIONALDISCLOSURETEXT:"+currentchat.FcraAdditionalDisclossureText+"  FCRAACKNOWLEDGEMENT : "+currentchat.FcraAcknowledgement +"  Do you agee?/y:[n]" 
                        currentchat.init_message = "FCRATEXT"
                        currentchat.save()
                        return reply
                elif result['Status'] == "Failure":
                    currentchat.init_message = "edit"
                    currentchat.save()
                    if "Invalid" in result['Message'] :
                        reply = "Your information did not pass out checks!"
                        return reply
                    elif "Validation error" in result['Message'] :
                        reply = "Oh no! WE couldn't validate your information."+str(result['ValidationErrors']) +"Please correct the error"
                        return reply
            else:
                reply = "Please enter yes/[no]"
                return reply

        elif currentchat.init_message == "FCRATEXT":
            if "y" in incoming_message:
                    currentchat.init_message = "CGMChecks"
                    currentchat.save()
                    return ("CGM Checks...")
        #start the flowchat5            
        elif currentchat.init_message == "CGMChecks":
            response = FLOWCHAT5(chatid)
            if response=="error":
                reply = "Oh no! Our System is having trouble wity your request"
                currentchat.init_message="help"
                currentchat.save()
                return reply
            elif response=="No-Pass":
                reply = "Sorry! We do not currently offer coverage in your area."
                currentchat.init_message = "End_chat"
                currentchat.save()
                reply = "End Chat here!"
                return reply
            elif response == "Pass":
                if currentchat.ResidenceState!="CA":
                    currentchat.init_message = "Lifeline"
                    currentchat.save()
                    reply = "Let's start Lisfeline"
                    return reply
                elif ConfirmState(chatid):
                    currentchat.init_message = "Lifeline"
                    currentchat.save()
                    reply = "Let's start Lisfeline"
                    return reply
                else:
                    currentchat.init_message = "ConfirmError"
                    currentchat.save()
                    reply = "Oh no! Our system is having trouble with your request"
                    return reply
        elif currentchat.init_message == "ConfirmError": 
           if "help" in incoming_message:
                reply = "An agent will  reach out  shortly!"
                return reply 
        elif currentchat.init_message == "help":
            if "help" in incoming_message:
                reply = "An agent will  reach out  shortly!"
                return reply             


                        

            


 
#     return reply

if __name__ == '__main__':
     generateReply(chatid,message)
    #generateReply(chatid,'STARTFLOWCHART3')