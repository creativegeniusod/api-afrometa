from rooms.models import Room, RoomUsers, RoomChat

""" Delete all rooms from db table """
def purgeChatRooms():
    status = False
    try:
        Room.objects.all().delete()
        status = True
    except:
        pass
    return status


""" Delete all chat history of rooms from db table """
def purgeRoomsChatHistory():
    status = False
    try:
        RoomChat.objects.all().delete()
        status = True
    except:
        pass
    return status



""" Delete all message History in db """
def purgeAllMessageHistory():
    status = False
    # try:
    #     RoomChat.objects.all().delete()
    #     status = True
    # except:
    #     pass
    return True
