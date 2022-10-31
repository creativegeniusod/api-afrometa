from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse

def index(request):
	""" Authenticated User. """
	if request.user.is_authenticated:
		
		context = {  }
		return render(request, 'charts/index.html', context)
	
	""" User not authenticated. """
	return render(request, 'dashboard_app/login.html')
