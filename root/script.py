import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time,os,uuid,json,re,sched, timeit,django  
from analyzer import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from root.models import ChatTracker


chatid = "O4U5YHRESL"
message = "Hello, how are u ?"
message = "THIS IS my zip code 40100"
message = "THIS IS my zip code mashood@gmail.com"

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
            reply = ["Hello! I am a bot here to help.","What is your Zip Code?"]
            print(reply)
            return reply  
        else:
            reply = ["Hello! I am a bot here to help.","What is your Zip Code?"]
            print(reply)
            return reply  

    elif currentchat.init_message !='':
        if currentchat.zipcode=='':
            # extract ZIP CODE
                zipcode = ZIPCODE_FINDER(incoming_message)
                if zipcode is not None: 
                    currentchat.zipcode=zipcode
                    currentchat.save()
                    reply = "What is your email address? (Ex: example@mail.com) "
                    print(reply)
                    return reply
                elif zipcode==None:
                    reply = "Please provide a valid ZipCode"
                    print(reply)
                    return reply
        

        elif len(str(currentchat.zipcode))==5:
            # extract phone number  
            email = EMAIL_FINDER(incoming_message)
            if email is not None:
                currentchat.email = email
                currentchat.save()
                reply = "YAY, Thank You! 🎉This will just take a few seconds 😊You are on your way to a FREE phone!"
                print(reply)
                return reply
            elif email is None:
                reply = "Please enter a valid Email Address"
                print(reply)
                return reply
#          


                
 
#     return reply

if __name__ == '__main__':
    generateReply(chatid,message)