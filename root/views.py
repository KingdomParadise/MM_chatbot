from django.http.response import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .script import  generateReply 

  


@csrf_exempt
def index(request): 
    if request.method=='POST':
        chatid = request.POST['chatid']
        message = request.POST['message']
 
        # print(chatid)
        reply = generateReply(chatid,message) 
        return JsonResponse({"message":reply})



