from django.http.response import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatTracker
from .script import generateReply


@csrf_exempt
def index(request):
    if request.method == 'POST':
        chatid = request.POST['chatid']
        message = request.POST['message']

        # print(chatid)
        reply = generateReply(chatid, message)
        return JsonResponse({"message": reply})


@csrf_exempt
def submit_info(request, id):
    items = ChatTracker.objects.filter(chatid=id)
    if len(items) == 0:
        return HttpResponse("<h1>Invalid User ID</h1>")
    else:
        item = items.first()
        if request.method == 'GET':
            if item.form_filled:
                return HttpResponse("<h1>Submitted :) </h1>")
            else:
                return render(request, 'root/index.html', {'id': id})
        if request.method == 'POST':
            program_value = request.POST['program_value']
            first_name = request.POST['first_name']
            middle_name = request.POST['middle_name']
            last_name = request.POST['last_name']
            second_last_name = request.POST['second_last_name']
            suffix = request.POST['suffix']
            date = request.POST['date']
            toggleaddress = 'toggleaddress' in request.POST.keys()
            apt_unit1 = request.POST['apt_unit1']
            apt_unit2 = request.POST['apt_unit2']
            address_nature = request.POST['address_nature']
            shipping_address = request.POST['shipping_address']
            residence_address = request.POST['residence_address']
            zipcode = request.POST['zipcode']
            last_four_social = request.POST['last_four_social']

            item.program = program_value
            item.first_name = first_name
            item.last_name = last_name
            item.middle_name = middle_name
            item.second_last_name = second_last_name
            item.suffix = suffix
            item.last_four_social = last_four_social
            item.address_nature = address_nature
            if toggleaddress is False:
                item.apt_unit1 = apt_unit1
                item.residential_address = residence_address
            else:
                item.apt_unit2 = apt_unit2
                item.shipping_address = shipping_address
                item.form_zip_code = zipcode

            item.form_filled = True
            item.save()
            print('==>>  Form Filled')

            return HttpResponse("<h1>Submitted :) </h1>")
