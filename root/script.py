import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time,os,uuid,json,re,sched, timeit,django  
from .analyzer import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from root.models import ChatTracker
from root.models import UserConfiguration
from root.models import StartOrder

chatid = "O4U5YHRESL"
message = "Hello, how are u ?"
message = "THIS IS my zip code 40100"
message = "THIS IS my zip code mashood@gmail.com"

def generateReply(chatid, incoming_message): 

    ischatidexist = ChatTracker.objects.filter(chatid=chatid).exists()
    if ischatidexist:pass
    else:ChatTracker(chatid=chatid).save()

    currentchat = ChatTracker.objects.get(chatid=chatid)
    avaliable_choices = ['inithello','irrelevent-int--force-zipcode','zipcode','email','user_configuration']
   
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
                    reply = "That Zip Code was not valid"
                    print(reply)
                    return reply
        

        #elif len(str(currentchat.zipcode))==5:
        elif currentchat.email=='':
            # extract phone number  
            email = EMAIL_FINDER(incoming_message)
            if email is not None:
                currentchat.email = email
                currentchat.save()
                reply = "Making sure that's a real email 💌  YAY, Thank You! 🎉This will just take a few seconds 😊You are on your way to a FREE phone!"
                print(reply)
                return reply
            elif email is None:
                reply = "Making sure that's a real email 💌  Please enter a valid Email Address"
                print(reply)
                return reply
    
def generateUserReply(token):
        currentchat = UserConfiguration.objects.get()
        currentchat.Token = token
        token = "d3a1b634-90a7-eb11-a963-005056a96ce9"   

        reply = "Hurray that was a valid zip code! 🎉"
                
        data = USER_CONFIGURATION_FINDER(token)
        
        currentchat.FirstName = data['FirstName']
        currentchat.lastName = data['LastName']
        currentchat.zipFilePassword = data['ZipFilePassword']
        currentchat.RequirePhoneNumber = data['RequirePhoneNumber']
        currentchat.RequireEmailAddress = data['RequireEmailAddress']
        currentchat.ReservationApiVersion = data['ReservationApiVersion']
        currentchat.ReservationUserCode = data['ReservationUserCode']
        currentchat.ReservationAgentCode = data['ReservationAgentCode']
        currentchat.ReservationClientCode = data['ReservationClientCode']
        currentchat.ReservationVenderCode = data['ReservationVenderCode']
        currentchat.ECommCaliforniaFlow = data['States']
        currentchat.Status = data['Status']
        currentchat.save()
        return reply
    
def generateStatementReply(Token,SerialNumber,Platform,AppVersion,State,SaleTypeId,Latitude,Longitude):
    currentchat = StartOrder.objects.get()  
    currentchat.Token = Token
    currentchat.SerialNumber = SerialNumber
    currentchat.platForm = Platform
    currentchat.platForm = AppVersion
    currentchat.State = State
    currentchat.saleTypeId = SaleTypeId
    currentchat.Latitude = Latitude
    currentchat.Longitude = Longitude

    reply = "Let's Start your FREE Application 😎"
    
    data = START_ORDERATION(Token,SerialNumber,Platform,AppVersion,State,SaleTypeId,Latitude,Longitude)
    
    currentchat.Result = data['Result']
    currentchat.OrderNumber = data['OrderNumber']
    currentchat.OrderDate = data['OrderDate']
    currentchat.PackageID = data['PackageId']
    currentchat.Status = data['Status']
    currentchat.Message = data['Message']
        
    currentchat.save()
    return reply

if __name__ == '__main__':
    generateReply(chatid,message)