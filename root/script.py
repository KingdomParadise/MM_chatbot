import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time,os,uuid,json,re,sched, timeit,django  
from analyzer import *
from CSGM_APIs import FLOWCHART3



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from root.models import ChatTracker


chatid = "O4U5YHR1ESL"
message = "Hello, how are u ?"
message = "THIS IS my zip code 40100"
message = "THIS IS my zip code 40100 mashood@gmail.com"


def CLEAR_ENTITY(currentchat):
    currentchat.zipcode=''
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
        if init_message in avaliable_choices:
            currentchat.init_message = init_message
            currentchat.save() 
            reply = ["Hello!👋 I am a bot and I am here to help.","What is your Zip Code?"]
            print(reply)
            return reply  
        else:
            reply = ["Hello!👋 I am a bot and I am here to help.","What is your Zip Code?"]
            print(reply)
            return reply  

    elif currentchat.init_message !='':
        if currentchat.zipcode=='':
            # extract ZIP CODE
                zipcode = ZIPCODE_FINDER(incoming_message)
                if zipcode is not None: 
                    currentchat.zipcode=zipcode
                    currentchat.save()
                    reply = "Great! That was a valid zip code! 🎉\nPlease enter your email address? (Ex: example@mail.com) 💬"
                    print(reply)
                    return reply
                elif zipcode==None:
                    reply = "That Zip Code was not valid. Please enter a valid zip code."
                    print(reply)
                    return reply
        

        elif len(str(currentchat.zipcode))==5 and currentchat.email=='':
            # extract phone number  
            email = EMAIL_FINDER(incoming_message)
            if email is not None:
                currentchat.email = email
                currentchat.save()
                reply = "Thank You! This will just take a few seconds You are on your way to a FREE phone!📱"
                currentchat.init_message = "STARTFLOWCHART3"
                currentchat.save()
                print(reply)
                print(currentchat.init_message)
                return reply
            elif email is None:
                reply = "That email address was not valid. Please enter a working email address. (Ex: example@mail.com)"
                print(reply)
                return reply

        #  HANDLING FLOWCHART 3
        elif currentchat.flowchart3_stucked_status is True:
            incoming_message = incoming_message.lower()
            if 're start' in incoming_message or 're-start' in incoming_message or 'restart' in incoming_message:
                print("--> KEYWORD Re-Start detected !")
                reply = 'Please enter a valid ZipCode.'
                print(reply)
                CLEAR_ENTITY(currentchat)
                return reply
            elif 'help' in incoming_message :
                print("--> KEYWORD HELP detected !")
                reply = 'An agent will reach out shortly! Thank you for your patience.'
                print(reply)
                return reply
            else:
                print("--> Neither HELP Nor RE-START detected !")
                reply = "Please type Restart to re-enter other valid information OR type Help to talk to our Agent"
                print(reply)
                return reply



        #  HANDLING FLOWCHART 3
        elif currentchat.init_message=='STARTFLOWCHART3':
            # email='denea1288@gmail.com'
            # email='denea128822@gmail.com'
            # zipcode=30314

            response = FLOWCHART3(currentchat.zipcode,currentchat.email)
            if response=='error_at_api1':
                reply = f'Sorry! We currently do not offer any service plans for the ZIP CODE {currentchat.zipcode} area. Please try with other ZipCode.'
                print(reply)
                CLEAR_ENTITY(currentchat)
                return reply
            elif response=='error_at_api2' or response=='error_at_api3' or response=='error_at_api4' :
                currentchat.flowchart3_stucked_status=True
                currentchat.save()
                reply = "Oh no! Our system is having trouble with your application. Please type Restart to re-enter valid information OR type Help to talk to our Agent."
                print(reply)
                return reply
            elif response=='send_link':
                reply = f'http://localhost:8000/submit_info/{chatid}'
                print(reply)
                return reply



                
 
#     return reply

if __name__ == '__main__':
     generateReply(chatid,message)
    #generateReply(chatid,'STARTFLOWCHART3')