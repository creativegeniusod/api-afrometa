from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from login_settings.models import LoginSettings
from . import SettingsHelper



def index(request):
    if request.user.is_authenticated:
        login_settings = LoginSettings.objects.all().order_by('-date_created')
        context = { 'login_settings': login_settings }
        return render(request, 'dashboard_app/login_settings/index.html', context)
    return render(request, 'dashboard_app/login.html')



def create(request):
    if request.user.is_authenticated:
        login_settings = LoginSettings.objects.all().order_by('-date_created')
        context = { 'login_settings': login_settings }
        if request.POST:
            option_name = request.POST.get('new-option')
            SettingsHelper.createNewOption(option_name)
        return render(request, 'dashboard_app/login_settings/index.html', context)
    return render(request, 'dashboard_app/login.html')



def settingUpdate(request, id):
    if request.user.is_authenticated:
        if request.POST:
            SettingsHelper.updateOption(request, id)
            context = {
                'login_settings': LoginSettings.objects.all().order_by('-date_created')
            }
            return render(request, 'dashboard_app/login_settings/index.html', context)
        login_settings = SettingsHelper.getObject(id)
        context = { 'option': login_settings }
        return render(request, 'dashboard_app/login_settings/edit.html', context)
    return render(request, 'dashboard_app/login.html')
