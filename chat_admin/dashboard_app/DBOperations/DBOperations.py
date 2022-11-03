from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from . import DbHelpers



def index(request):
    context = {  }
    return render(request, 'dashboard_app/db_operations/index.html', context)


def purge(request):
    data = {
		'status': False
	}
    req_status = 500

    if request.POST:
        if request.user.is_authenticated:

            status = False
            op = request.POST.get('op')
            if op == "cr":
                status = DbHelpers.purgeChatRooms()
            elif op == "rch":
                status = DbHelpers.purgeRoomsChatHistory()
            elif op == "amh":
                status = DbHelpers.purgeAllMessageHistory()

            data = {
    			'status': True,
    			'message': 'Request success'
    		}
            req_status = 200
    return JsonResponse(data, status=req_status)
