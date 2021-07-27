#from django.db.models.enums import IntegerChoices
from root.analyzer import CGMChecks, EDIT_Info, EDIT_Info_item, FCRATEXT, GET_FLOWCHAT_STATE, SAVE_Info, SET_ConfirmInfo, SET_TribalResident, STARTFLOWCHAT4, setLanguageEs , setLanguageJv ,setLanguageCK 
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time,os,uuid,json,re,sched, timeit,django  
from analyzer import *
from CSGM_APIs import CheckAvailability_API, UserConfiguration_API, StateConfiguration_API, StartOrder_API, Lifeline_API, CheckNVApplicationStatus_API,CheckNladEbbApplicationStatus_API



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

    if currentchat.init_message=='':
        init_message = INIT_MESSAGE_HANDLER(incoming_message) 
        return get_start(chatid,init_message)
    elif currentchat.init_message !='':
        if currentchat.ResidenceZip=='':
            return   ZIPCODE_FINDER(chatid,incoming_message)
        elif currentchat.init_message =="Get_email":
           return  EMAIL_FINDER(chatid,incoming_message)  
        elif currentchat.flowchart3_stucked_status is True:
            incoming_message = incoming_message.lower()
            return GET_FLOWCHAT_STATE(incoming_message,chatid)
        elif currentchat.init_message=='STARTFLOWCHART3':
            check = CheckAvailability_API(currentchat.ResidenceZip,currentchat.email)
            if check:
                userConfiguration = UserConfiguration_API(chatid)
                if userConfiguration:
                    currentchat.ReservationUserCode = userConfiguration['ReservationUserCode']
                    currentchat.ReservationAgentCode = userConfiguration['ReservationAgentCode']
                    currentchat.ReservationClientCode = userConfiguration['ReservationClientCode']
                    currentchat.ReservationVendorCode = userConfiguration['ReservationVendorCode']
                    currentchat.save()
                    stateConfiguration = StateConfiguration_API(chatid)                  
                    if stateConfiguration:
                        if currentchat.ResidenceState == "CA":
                            currentchat.TribalEligible = stateConfiguration['TribalEligible']
                            currentchat.FcraDisclosureText = stateConfiguration['FcraDisclosureText']
                            currentchat.FcraAdditionalDisclosureText = stateConfiguration['FcraAdditionalDisclosureText']
                            currentchat.FcraAcknowledgement = stateConfiguration['FcraAcknowledgement']
                            currentchat.EligibiltyPrograms = stateConfiguration['EligibiltyPrograms'][0]['Code']
                            currentchat.save()
                        else:
                            currentchat.TribalEligible = stateConfiguration['TribalEligible']
                            currentchat.EligibiltyPrograms = stateConfiguration['EligibiltyPrograms'][0]['Code']
                            currentchat.save()
                        startOrder = StartOrder_API(chatid)
                        if startOrder:
                                currentchat.OrderNumber = startOrder['OrderNumber']
                                currentchat.PackageId = startOrder['PackageId']
                                currentchat.save()
                                currentchat.init_message = "STARTFLOWCHART4"
                                currentchat.save()
                                print(currentchat.ReservationUserCode)
                                print(currentchat.ReservationVendorCode)
                                print(currentchat.PackageId)
                                print(currentchat.EligibiltyPrograms)

                                return [f'http://localhost:8000/submit_info/{chatid}','url']
                        
                currentchat.flowchart3_stucked_status=True
                currentchat.save()
                return ["Oh no! Our system is having trouble with your application","normal_restart_help"]
            else:
                CLEAR_ENTITY(currentchat)
                return [f'Sorry! We currently do not offer any service plans for the ZIP CODE {currentchat.ResidenceZip} area. Please try with other ZipCode. : Enter zip code again!','normal']
            
        elif currentchat.init_message == 'STARTFLOWCHART4':
            return STARTFLOWCHAT4(chatid)
        elif currentchat.init_message == "TribalResident":
            return SET_TribalResident(incoming_message,chatid) 
        elif currentchat.init_message == "Confirm_information":   
            return SET_ConfirmInfo(chatid)
        elif currentchat.init_message == "edit":
            return EDIT_Info(incoming_message,chatid)      
        elif currentchat.init_message == "edit_item":
            return EDIT_Info_item(incoming_message,chatid)
        elif currentchat.init_message == "save_item":
            return SAVE_Info(incoming_message,chatid)
        elif currentchat.init_message == "FCRATEXT":
            return FCRATEXT(incoming_message,chatid)
        #start the flowchat5            
        elif currentchat.init_message == "CGMChecks":
            return CGMChecks(chatid)
        elif currentchat.init_message == "ConfirmError": 
           if "help" in incoming_message:
                reply = ["An agent will  reach out  shortly!","normal"]
                return reply 
        elif currentchat.init_message == "help":
            if "help" in incoming_message:
                reply = ["An agent will  reach out  shortly!","normal"]
                return reply  
        elif currentchat.init_message == "Lifeline":
            response = Lifeline_API(chatid)
            return Lifeline_state(response,chatid)      
        elif currentchat.init_message=="lifeline_success":
            return lifeline_success(chatid)
        elif currentchat.init_message == "setLanguageEs":
            return setLanguageEs(chatid,incoming_message)
        elif currentchat.init_message == "setLanguageCk":
            return setLanguageCK(chatid,incoming_message)
        elif currentchat.init_message == "setLanguageJv":
            return setLanguageJv(chatid,incoming_message)
        elif currentchat.init_message == "lifeline_failure":
            currentchat.init_message = "agent_help"
            currentchat.save()
            return ["An agent will reach out shortly! Thank you for your patience.","normal_help"]  
        elif  currentchat.init_message == "check_status_lifeline":
                if currentchat.ResidenceChat=="CA":
                    response = CheckNladEbbApplicationStatus_API() 
                    return          
                else:
                    response = CheckNVApplicationStatus_API()
                    return          


                        

            


 
#     return reply

if __name__ == '__main__':
     generateReply(chatid,message)