from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.models import User
from rooms.models import Room, RoomUsers, RoomChat
from votes.models import SiteVote
from wallet.models import UserWallet, Wallet
from login_settings.models import LoginSettings
from .helpers import Helper

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]



@csrf_exempt
def createUser(request):
	data = {
		'status': False
	}

	if request.method == 'POST':
		req_data = json.loads(request.body.decode('utf-8'))

		username = req_data.get('username')
		email = req_data.get('email')
		fullname = ''
		password = ''
		wallet = ''

		if 'fullname' in req_data:
			fullname = req_data.get('fullname')
		if 'password' in req_data:
			password = req_data.get('password')
		if 'wallet_id' in req_data:
			wallet = req_data.get('wallet_id')
			username = wallet[:4] + '...' + wallet[-4:]
			email = wallet[:4] + '...' + wallet[-4:] + '@walletuser.com'

		if password == '' or password is None:
			password = 'DummyUserPassword@098~!'

		try:
			username = username.lower()
			user = User.objects.create_user(username=username, email=email, password=password)
			user.save()

			if wallet:
				try:
					walletUser = UserWallet.objects.get(wallet=wallet)
				except Exception as e:
					walletUser = UserWallet(user=user, wallet=wallet)
					walletUser.save()

		except Exception as e:
			print('e: ', e)
			return JsonResponse(data)

		data = {
			'status': True,
			'username': username,
			'email': email
		}

	return JsonResponse(data)


@csrf_exempt
def userLookup(request, username):
	data = { 'status': False }
	res_status = 417

	try:
		user = User.objects.get(username=username)
		data['status'] = True
		data['user'] = {
			'username': user.username,
			'email': user.email,
			'is_active': user.is_active
		}
		res_status = 200
	except Exception as e:
		data['exception'] = str(e)
		pass

	return JsonResponse(data, content_type='application/json', status=res_status)

@csrf_exempt
def userSearch(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':
		req_data = json.loads(request.body.decode('utf-8'))
		try:
			username = req_data.get('username')
			username = username.lower()

			try:
				user = User.objects.get(username=username)
				data['status'] = True
				data['user'] = {
					'username': user.username,
					'email': user.email,
					'is_active': user.is_active
				}
				res_status = 200
			except Exception as e:
				data['exception'] = str(e)
				res_status = 500
				pass

		except:
			data['message'] = 'Required parameters not provided.'

	return JsonResponse(data, content_type='application/json', status=res_status)

@csrf_exempt
def createRoom(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':
		req_data = json.loads(request.body.decode('utf-8'))
		room_name = req_data.get('room_name')
		room_id = req_data.get('room_id')
		owner = req_data.get('createdBy')
		users = req_data.get('users')

		try:
			user = User.objects.get(username=owner)

			try:
				room = Room(name=room_name, room_id=room_id, owner=user)
				room.save()

				r = Room.objects.get(room_id=room_id)
				res_status = 201

				if len(users) > 0:
					for u in users:
						try:
							user_ins = User.objects.get(username=u)
							room_users = RoomUsers(user=user_ins, room=room)
							room_users.save()
						except Exception as e:
							res_status = 417
							pass
			except Exception as e:
				pass

			data['status'] = True
			data['data'] = {
				'room_name': room_name,
				'room_id': room_id,
				'room_owner': owner,
				'users': users
			}
		except Exception as e:
			pass
	else:
		data['message'] = 'Method not allowed'

	return JsonResponse(data, content_type='application/json', status=res_status)


@csrf_exempt
def saveRoomMessage(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':

		req_data = json.loads(request.body.decode('utf-8'))
		message_to = req_data.get('to')
		message_from = req_data.get('from')
		message = req_data.get('message')
		sent_at = req_data.get('time_of_message')

		try:
			user = User.objects.get(username=message_from)
			room = Room.objects.get(room_id=message_to)

			try:
				room_message = RoomChat(message=message, message_from=user, room=room, sent_time=sent_at)
				room_message.save()
				res_status = 201
				data['status'] = True
			except Exception as e:
				print('Stage 12 *****************************', e)
				pass
		except Exception as e:
			print('Stage 1 *****************************', e)
			pass
	else:
		data['message'] = 'Method not allowed'

	return JsonResponse(data, content_type='application/json', status=res_status)



@csrf_exempt
def addNewUsers(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':
		users_added = 0

		req_data = json.loads(request.body.decode('utf-8'))
		room_id = req_data.get('room_id')
		new_users = req_data.get('new_users')

		try:
			room = Room.objects.get(room_id=room_id)

			if len(new_users) > 0:
				res_status = 201
				for new_user in new_users:
					user = User.objects.get(username=new_user)
					try:
						user_in_room = RoomUsers.objects.get(user=user, room=room)
						data['status'] = True
					except Exception as e:
						try:
							add_new_user = RoomUsers(user=user, room=room)
							add_new_user.save()
							data['status'] = True
							users_added += 1
						except Exception as e:
							pass
				data['users_requested'] = len(new_users)
				data['users_added'] = users_added
		except Exception as e:
			pass
	else:
		data['message'] = 'Method not allowed'

	return JsonResponse(data, content_type='application/json', status=res_status)


@csrf_exempt
def getRoomMessages(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':

		req_data = json.loads(request.body.decode('utf-8'))
		room_id = req_data.get('room_id')
		try:
			room = Room.objects.get(room_id=room_id)
			messages = []
			try:
				m = RoomChat.objects.filter(room=room)
				for message in m:
					messages.append({
						'message': message.message,
						'from': message.message_from.username,
						'to': message.room.room_id,
						'sent_time': message.sent_time
					})
			except Exception as e:
				print('empty')

			data['status'] = True
			data['messages'] = messages
			res_status = 200
		except Exception as e:
			print('Stage 1 *******************', e)
			pass
	else:
		data['message'] = 'Method not allowed'

	return JsonResponse(data, content_type='application/json', status=res_status)


"""
Data['code'] = 1/2
1 = room Created
2 = room Found
"""
@csrf_exempt
def pageRoom(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':
		req_data = json.loads(request.body.decode('utf-8'))
		url = req_data['url']
		requested_user = req_data['user']
		isSiteRoom = req_data['isSiteRoom']
		domain = Helper.urlToDomain(url)
		clean_url = url.split('?')[0]
		new_user_added = False

		if isSiteRoom:
			room_id = Helper.domainToRoomId(domain)
			room_name = domain
		else:
			room_id = req_data['room_id']
			room_name = clean_url

		try:
			""" Room already there. """
			room = Room.objects.get(room_id=room_id)
			room_messages = RoomChat.objects.filter(room=room)


			try:
				user = User.objects.get(username=requested_user['username'])

				""" find or save room user. """
				try:
					RoomUsers.objects.get(room=room, user=user)
				except:
					room_user = RoomUsers(user=user, room=room)
					room_user.save()
					new_user_added = True

			except Exception as e:
				print('**********Error here*****', e)


			""" Get all room users. """
			room_users = RoomUsers.objects.filter(room=room)


			""" simplify room data for browsers. """
			room_simplified = Helper.roomSimplified(room, room_messages, room_users)
			data['status'] = True
			data['message'] = 'Room found'
			data['room'] = room_simplified
			data['code'] = '2'
			data['new_user_added'] = new_user_added
			data['isSiteRoom'] = isSiteRoom
			res_status = 200

		except:
			""" Create new page room """
			try:
				user = User.objects.get(username='admin')

				room = Room(name=room_name, room_id=room_id, owner=user, clean_url=clean_url)
				room.save()

				# Add first user to room.
				first_room_user = User.objects.get(username=requested_user['username'])

				# add user to room_users table.
				room_user = RoomUsers(user=first_room_user, room=room)
				room_user.save()

				""" Get all room users. """
				room_users = RoomUsers.objects.filter(room=room)

				room_simplified = Helper.roomSimplified(room, [], room_users)
				data['status'] = True
				data['message'] = 'Room Created.'
				data['room'] = room_simplified
				data['code'] = '1'
				data['new_user_added'] = False
				data['isSiteRoom'] = isSiteRoom
				res_status = 200
			except Exception as e:
				print('***** Error creating same site room:::::', e)
				data['message'] = "Error creating same site room"


	return JsonResponse(data, content_type='application/json', status=res_status)


""" Cast User Vote on a Site. """
@csrf_exempt
def castSiteVote(request, vote):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':
		req_data = json.loads(request.body.decode('utf-8'))

		try:
			username = req_data['username']
			page = req_data['page']
			domain = req_data['domain']

			user = User.objects.get(username=username)

			try:
				userVote = SiteVote.objects.get(page=page, user=user)
				userVote.vote = vote
				userVote.save()
				pass
			except Exception as e:
				userVote = SiteVote(page=page, vote=vote, user=user, domain=domain)
				userVote.save()

			upVotes = SiteVote.objects.filter(page=page).filter(vote=True).count()
			totalVotes = SiteVote.objects.filter(page=page).count()
			pageScore = int (( upVotes / totalVotes ) * 100)

			data['status'] = True
			data['message'] = str('We have saved your vote for this page.')
			data['pageScore'] = pageScore
			res_status = 200

		except Exception as e:
			data['message'] = str('There is some error saving your vote.')

	return JsonResponse(data, content_type='application/json', status=res_status)



""" Page Score """
@csrf_exempt
def getPageScore(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':
		req_data = json.loads(request.body.decode('utf-8'))

		try:
			page = req_data['page']
			upVotes = SiteVote.objects.filter(page=page).filter(vote=True).count()
			totalVotes = SiteVote.objects.filter(page=page).count()

			pageScore = int (( upVotes / totalVotes ) * 100)

			data['status'] = True
			data['pageScore'] = pageScore
			data['message'] = str('Page Score Calculated.')
			res_status = 200

		except Exception as e:
			data['message'] = str('There are no page score.')

	return JsonResponse(data, content_type='application/json', status=res_status)


""" Wallet Info """
@csrf_exempt
def getWalletInfo(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':
		res_status = 200
		req_data = json.loads(request.body.decode('utf-8'))
		wallet_type = None
		wallet_active_type = None
		if 'type' in req_data:
			wallet_type = req_data['type']

		if 'activeType' in req_data:
			wallet_active_type = req_data['activeType']

		if wallet_type is not None and wallet_active_type is not None:
			try:
				wallet_info = Wallet.objects.get(type=wallet_type, activeType=wallet_active_type)
				data['status'] = True
				data['wallet'] = {
					'id': wallet_info._id,
					'type': wallet_info.type,
					'activeType': wallet_info.activeType,
					'whiteListedNFTaddresses': wallet_info.whiteListedNFTaddresses
				}
				data['message'] = str('Request Completed.')
			except:
				data['message'] = str('There is nothing to show.')
		elif wallet_type is not None:

			try:
				wallet_info = Wallet.objects.get(type=wallet_type)
				data['status'] = True
				data['wallet'] = {
					'type': wallet_info.type,
					'activeType': wallet_info.activeType,
					'whiteListedNFTaddresses': wallet_info.whiteListedNFTaddresses
				}
				data['message'] = str('Request Completed.')
			except Exception as e:
				print('EEE: ', e)
				data['message'] = str('There is nothing to show.')
		elif wallet_active_type is not None:
			try:
				wallet_info = Wallet.objects.get(activeType=wallet_active_type)
				data['status'] = True
				data['wallet'] = {
					'id': wallet_info._id,
					'type': wallet_info.type,
					'activeType': wallet_info.activeType,
					'whiteListedNFTaddresses': wallet_info.whiteListedNFTaddresses
				}
				data['message'] = str('Request Completed.')
			except:
				data['message'] = str('There is nothing to show.')


	return JsonResponse(data, content_type='application/json', status=res_status)

""" User's wallet info """
@csrf_exempt
def getUserWalletInfo(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':
		try:
			req_data = json.loads(request.body.decode('utf-8'))
			username = req_data['username']

			user = User.objects.get(username=username)

			try:
				uw = UserWallet.objects.get(user=user)
				data['wallet_address'] = uw.wallet
			except Exception as ee:
				data['wallet_address'] = None

			data['status'] = True
			res_status = 200
		except Exception as e:
			data['exception'] = str(e)
			pass

	return JsonResponse(data, content_type='application/json', status=res_status)


""" Get or Post wallet status """
@csrf_exempt
def walletStatus(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':
		res_status = 200
		req_data = json.loads(request.body.decode('utf-8'))
		active_type = None
		if 'activeType' in req_data:
			active_type = req_data['activeType']

		try:
			wallet_info = Wallet.objects.get(type='activeType')
			wallet_info.activeType = active_type
			wallet_info.save()

			data['status'] = True
			data['message'] = str('Request Completed.')
		except Exception as e:
			data['message'] = str('There is nothing to show.')
			# try:
			# 	info = Wallet.objects.get(type='activeType')
			# except Exception as e:
			# 	new_wallet = Wallet(type='activeType', activeType=active_type, whiteListedNFTaddresses="")
			# 	new_wallet.save()
			#
			# 	data['status'] = True
			# 	data['message'] = str('Request Completed.')
	elif request.method == 'GET':
		res_status = 200
		try:
			wallet_info = Wallet.objects.get(type='activeType')
			data['status'] = True
			data['wallet'] = {
				'activeType': wallet_info.activeType,
				'whitelist': Helper.whiteListedArray(wallet_info.whiteListedNFTaddresses)
			}
			data['message'] = str('Request Completed.')
		except Exception as e:
			data['message'] = str('There is nothing to show.')

	return JsonResponse(data, content_type='application/json', status=res_status)


""" Add Whitelist values """
@csrf_exempt
def walletAddWhitelist(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':
		res_status = 200
		req_data = json.loads(request.body.decode('utf-8'))

		nftAddress = None
		if 'nftAddress' in req_data:
			nftAddress = req_data['nftAddress']

		if nftAddress is not None and nftAddress != "":
			try:
				wallet_info = Wallet.objects.get(type='activeType')
				wallet_info.whiteListedNFTaddresses = Helper.addToWhitelist(wallet_info.whiteListedNFTaddresses, nftAddress)
				wallet_info.save()

				data['status'] = True
				data['message'] = str('Request Completed.')
			except Exception as e:
				data['message'] = str('There is nothing to show.')
		else:
			data['message'] = str('There is nothing to show.')
	return JsonResponse(data, content_type='application/json', status=res_status)


""" Remove Whitelist values """
@csrf_exempt
def walletRemoveWhitelist(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'POST':
		res_status = 200
		req_data = json.loads(request.body.decode('utf-8'))

		nftAddress = None
		if 'nftAddress' in req_data:
			nftAddress = req_data['nftAddress']

		if nftAddress is not None and nftAddress != "":
			try:
				wallet_info = Wallet.objects.get(type='activeType')
				wallet_info.whiteListedNFTaddresses = Helper.removeFromWhitelist(wallet_info.whiteListedNFTaddresses, nftAddress)
				wallet_info.save()

				data['status'] = True
				data['message'] = str('Request Completed.')
			except Exception as e:
				data['message'] = str('There is nothing to show.')
		else:
			data['message'] = str('There is nothing to show.')
	return JsonResponse(data, content_type='application/json', status=res_status)


""" Get Sign in/up Options """
def getSignOptions(request):
	data = { 'status': False }
	res_status = 417

	if request.method == 'GET':
		res_status = 200

		options = LoginSettings.objects.filter(status=True).values('id', 'name')
		data['status'] = True
		data['message'] = str('Request Completed.')
		data['options'] = list(options)
	return JsonResponse(data, content_type='application/json', status=res_status)
