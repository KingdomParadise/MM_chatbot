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
@csrf_exempt
def userConfigurate(request):
    if request.method=='POST':
        token = request.POST['token']
        print(token)
        reply = generateUserReply(token)
        return JsonResponse(reply)
@csrf_exempt
def orderStatement(request):
    if request.method=='POST':
        Token = request.POST['Token']
        SerialNumber = request.POST['SerialNumber']
        Platform = request.POST['Platform']
        AppVersion = request.POST['AppVersion']
        State = request.POST['State']
        SaleTypeId = request.POST['SaleTypeId']
        Latitude = request.POST['Latitude']
        Longitude = request.POST['Longitude']      
        
        reply = generateStatementReply(Token,SerialNumber,Platform,AppVersion,State,SaleTypeId,Latitude,Longitude)

        return JsonResponse(reply)
        
          
        