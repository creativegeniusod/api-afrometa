from login_settings.models import LoginSettings

def createNewOption(name):
    # room_message = RoomChat(message=message, message_from=user, room=room, sent_time=sent_at)
    try:
        new_setting = LoginSettings(name=name, status=True)
        new_setting.save()
        return True
    except:
        return False


def getObject(id):
    try:
        ls = LoginSettings.objects.get(id=id)
        return ls
    except:
        return None


def updateOption(request, id):
    try:
        name = request.POST.get('name')
        status = request.POST.get('status')
        LoginSettings.objects.filter(id=id).update(status=status)
        return True
    except:
        return False
