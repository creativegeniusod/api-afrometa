from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, logout, login
from django.dispatch import receiver
from django.db.models.signals import pre_save

# import models
from django.contrib.auth.models import User
from .models import Permission
from rooms.models import Room, RoomUsers, RoomChat
from votes.models import SiteVote

# import forms
from .forms import EditProfile, SignUp



""" Index route. default to list users or login page """
def index(request):
	""" Authenticated User. """
	if request.user.is_authenticated:
		users = User.objects.all().order_by('-date_joined')
		context = { 'users': users }
		return render(request, 'dashboard_app/users.html', context)
	
	""" User not authenticated. """
	return render(request, 'dashboard_app/login.html')


""" Login Submit """
def loginAction(request):
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password, is_superuser=True)
		if user is not None:
			login(request, user)
			return redirect('users')
		else:
			return redirect('index')


""" Logout a user. """
def userLogout(request):
    logout(request)
    return redirect('index')
		


""" List all users """
def users(request):
	if request.user.is_authenticated:
		users = User.objects.all().order_by('-date_joined')
		context = { 'users': users }
		return render(request, 'dashboard_app/users.html', context)

	return redirect('index')

def wallet(request):
	if request.user.is_authenticated:
		users = User.objects.all().order_by('-date_joined')
		context = { 'users': users }
		return render(request, 'dashboard_app/wallet.html', context)

	return redirect('index')

""" create new user """
def userSave(request):
	
	data = {
		'status': False
	}

	if request.POST:
		username = request.POST.get('username')
		fullname = request.POST.get('fullname')
		email = request.POST.get('email')
		password = request.POST.get('password')

		if password == '' or password is None:
			password = 'DummyUserPassword@098~!'

		user = User.objects.create_user(username, email, password)
		user.save()

		data = {
			'status': True,
			'username': username,
			'email': email
		}

	return JsonResponse(data)



""" Show a user. """
def userView(request, username):
	if request.user.is_authenticated:
		user = User.objects.get(username=username)
		context = { 'user': user }
		return render(request, 'dashboard_app/user.html', context)
	return redirect('index')



""" Edit a user. """
def userEdit(request, username):
	if request.user.is_authenticated:
		if request.method == 'POST':
			user = User.objects.get(username=username)
			form = EditProfile(request.POST, instance=user)
			form.actual_user = request.user

			if form.is_valid():
				new_username = form['username'].value()
				form.save()
				return redirect('user_view', username=new_username)
			else:
				context = { 'form': form, 'user': user }
				return render(request, 'dashboard_app/user-edit.html', context)
		else:
			user = User.objects.get(username=username)
			form = EditProfile(instance=user)
			context = { 'form': form, 'user': user }
			return render(request, 'dashboard_app/user-edit.html', context)
	else:
		return redirect('index')



""" Delete a non-superuser user. """
def userDelete(request, username):
	data = {
		'status': False
	}
	res_status = 417

	try:
		user = User.objects.get(username=username)

		""" Proceed if user to be deleted is not superuser. """
		if not user.is_superuser:
			delete_rooms = []
			update_room_admin = {}
			rooms = Room.objects.filter(owner=user)
			for room in rooms:
				new_room_admin = RoomUsers.objects.filter(room=room).first()
				if new_room_admin is None: # delete this room
					delete_rooms.append(room)
				else: # assign other admin to the room.
					update_room_admin[room.room_id] = new_room_admin
				pass

			""" Delete empty rooms created by deleting user. """
			if len(delete_rooms) > 0:
				for room in delete_rooms:
					RoomUsers.objects.filter(room=room).delete()
					RoomChat.objects.filter(room=room).delete()
					Room.objects.get(room_id=room.room_id).delete()
					pass


			""" Update room admin """
			if len(update_room_admin) > 0:
				for room in Room.objects.filter(owner=user):
					''' update room admin. '''
					room.owner = update_room_admin[room.room_id].user
					room.save()

					''' delete user from roomUsers collection '''
					RoomUsers.objects.get(user=update_room_admin[room.room_id].user, room=room).delete()
					pass

			""" Delete requested User. """
			try:
				user.delete()
				data['message'] = str('User Deleted Successfully.')
				data['status'] = True
				res_status = 200
			except Exception as e:
				data['exception'] = str(e)
				pass
		else:
			data['message'] = str('This user has special permissions and preventing user from deleting.')
			pass
	except Exception as e:
		data['exception'] = str(e)
		pass

	return JsonResponse(data, content_type='application/json', status=res_status)



"""
	Signal. to mark user inactive, in case of new user.
	replace space with underscore
"""
@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
	
	if instance._state.adding is True:
		
		if ' ' in instance.username:
			username = instance.username
			instance.username = username.replace(' ', '_')
			

		if not instance.is_superuser:
			instance.is_active = False


""" User Sign Up. """
def userSignUp(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			form = SignUp(request.POST)
			form.actual_user = request.user

			if form.is_valid():
				new_username = form['username'].value(  )
				form.save()
				return redirect('index')
			else:
				return render(request, 'dashboard_app/signup.html', { 'form': form })
		
		else:
			form = SignUp(request.POST)
			return render(request, 'dashboard_app/signup.html', {'form': form})

	return redirect('users/')



""" User Activate """
def userActivate(request):
	data = {
		'status': False
	}
	if request.POST:
		if request.user.is_authenticated:
			username = request.POST.get('username')
			user = User.objects.get(username=username)

			user.is_active = True
			user.save()

			data = {
				'status': True
			}

	return JsonResponse(data)



""" User Permissions """
def userPermissions(request):
	# return JsonResponse({ 'status': True, 'page': 'Permissions' })

	permissions = Permission.objects.all().order_by('-date_created')
	context = { 'permissions': permissions }
	return render(request, 'dashboard_app/permissions.html', context)



def userPermissionCreate(request):
	if request.POST:
		if request.user.is_authenticated:
			name = request.POST.get('permission')
			permission = Permission(name=name, created_by=request.user)
			permission.save()
			return redirect('user_permissions')

	context = {}
	return render(request, 'dashboard_app/permissions/create.html', context)



def listRooms(request):
	context = {}
	try:
		rooms = Room.objects.all().order_by('-date_created')
		context['rooms'] = rooms
	except Exception as e:
		pass

	return render(request, 'dashboard_app/rooms/index.html', context)
	

def pageVotes(request):
	context = {}
	try:
		all_votes = SiteVote.objects.order_by('-date_created').values('page', 'domain').distinct()
		votes = []
		done = []
		
		for vote in all_votes:
			if vote['page'] != 'invalid page':
				if vote['page'] not in done:
					done.append(vote['page'])
					totalVotes = SiteVote.objects.filter(page=vote['page']).count()
					upVotes = SiteVote.objects.filter(page=vote['page'], vote=True).count()
					score = int (( upVotes / totalVotes ) * 100)
					
					abc = {
						'page': vote['page'],
						'domain': vote['domain'],
						'totalVotes': totalVotes,
						'upVotes': upVotes,
						'score': score
					}
					votes.append(abc)

		context['votes'] = votes
	except Exception as e:
		pass

	return render(request, 'dashboard_app/votes/index.html', context)
	
def PrivacyPolicy(request):
	return render(request, 'dashboard_app/privacy-policy.html')
	
def TermsOfService(request):
	return render(request, 'dashboard_app/terms-of-service.html')
