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
   
    print (chatid, incoming_message)
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
                    reply = ["What is your email address? (Ex: example@mail.com) "]
                    print(reply)
                    return reply
                elif zipcode==None:
                    reply = ["That Zip Code was not valid"]
                    print(reply)
                    return reply
        

        #elif len(str(currentchat.zipcode))==5:
        elif currentchat.email=='':
            # extract phone number  
            email = EMAIL_FINDER(incoming_message)
            if email is not None:
                currentchat.email = email
                currentchat.save()
                reply = ["Making sure that's a real email 💌","  YAY, Thank You! 🎉","This will just take a few seconds 😊You are on your way to a FREE phone!"]
                print(reply)
                return reply
            elif email is None:
                reply = ["Making sure that's a real email 💌 "," Please enter a valid Email Address"]
                print(reply)
                return reply
    
def generateUserReply(token):
        data = USER_CONFIGURATION_FINDER(token)

        reply = {"message":"Hurray that was a valid zip code! 🎉",
                 "FirstName":data['FirstName'],
                 "LastName":data['LastName'],
                 "ZipFilePassword":data['ZipFilePassword'],
                 "RequirePhoneNumber":data['RequirePhoneNumber'],
                 "RequireEmailAddress":data['RequireEmailAddress'],
                 "ReservationApiVersion":data['ReservationApiVersion'],
                 "ReservationUserCode":data['ReservationUserCode'],
                 "ReservationAgentCode":data['ReservationAgentCode'],
                 "ReservationClientCode":data['ReservationClientCode'],
                 "ReservationVendorCode":data['ReservationVendorCode'],
                 "States":data['States'],
                 "Status":data['Status'],
        }
        
      #  currentchatuser.FirstName = data['FirstName']
      #  currentchatuser.lastName = data['LastName']
      #  currentchatuser.zipFilePassword = data['ZipFilePassword']
      #  currentchatuser.RequirePhoneNumber = data['RequirePhoneNumber']
      #  currentchatuser.RequireEmailAddress = data['RequireEmailAddress']
      #  currentchatuser.ReservationApiVersion = data['ReservationApiVersion']
      #  currentchatuser.ReservationUserCode = data['ReservationUserCode']
      #  currentchatuser.ReservationAgentCode = data['ReservationAgentCode']
      #  currentchatuser.ReservationClientCode = data['ReservationClientCode']
      #  currentchatuser.ReservationVenderCode = data['ReservationVenderCode']
      #  currentchatuser.ECommCaliforniaFlow = data['States']
      #  currentchatuser.Status = data['Status']
      #  currentchatuser.save()

        return reply
    
def generateStatementReply(Token,SerialNumber,Platform,AppVersion,State,SaleTypeId,Latitude,Longitude):
    #currentchat = StartOrder.objects.get()  
    #currentchat.Token = Token
    #currentchat.SerialNumber = SerialNumber
    #currentchat.platForm = Platform
    #currentchat.platForm = AppVersion
    #currentchat.State = State
    #currentchat.saleTypeId = SaleTypeId
    #currentchat.Latitude = Latitude
    #currentchat.Longitude = Longitude


    print("dfdf")
    data = START_ORDERATION(Token,SerialNumber,Platform,AppVersion,State,SaleTypeId,Latitude,Longitude)
    
    #currentchat.Result = data['Result']
    #currentchat.OrderNumber = data['OrderNumber']
    #currentchat.OrderDate = data['OrderDate']
    #currentchat.PackageID = data['PackageId']
    #currentchat.Status = data['Status']
    #currentchat.Message = data['Message']
        
    #currentchat.save()
    print(data)
    reply = {"message":"Let's Start your FREE Application 😎",
              "Result":data['Result'],
              "OrderDate":data['OrderDate'],
              "PackageID":data['PackageId'],
              "Status":data['Status'],
              "Message":data['Message'],
    }
    return reply

if __name__ == '__main__':
    generateReply(chatid,message)