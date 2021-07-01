from django.http.response import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .script import  generateReply , generateUserReply , generateStatementReply

  


@csrf_exempt
def index(request): 
    if request.method=='POST':
        chatid = request.POST['chatid']
        message = request.POST['message']
        
        reply = generateReply(chatid,message) 
        return JsonResponse({"message":reply})

def userConfigurate(request):
    if request.method=='POST':
        token = request.post['token']
        
        reply = generateUserReply(token)
        return JsonResponse({"message":reply})

def orderStatement(request):
    if request.method=='POST':
        Token = request.POST['token']
        SerialNumber = request.POST['serialNumber']
        Platform = request.POST['platForm']
        AppVersion = request.POST['appVersion']
        State = request.POST['state']
        SaleTypeId = request.POST['saleTypeId']
        Latitude = request.POST['latitude']
        Longitude = request.POST['longitude']      
        
        reply = generateStatementReply(Token,SerialNumber,Platform,AppVersion,State,SaleTypeId,Latitude,Longitude)
        
        return JsonResponse({"message":reply})
          
        