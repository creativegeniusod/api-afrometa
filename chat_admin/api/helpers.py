from urllib.parse import urlparse

class Helper:

	""" extract domain from supplied url. """
	def urlToDomain(url):
		return url if url == "" else urlparse(url).netloc

	""" convert room_id to domain. """
	def domainToRoomId(domain):
		return domain if domain == "" else domain.replace(".", "__")

	""" convert room properties to simplified. """
	def roomSimplified(room, messages=[], users=[]):
		msg_parsed = []
		users_parsed = []
		for message in messages:
			msg_parsed.append({
				'message': message.message,
				'sent_time': message.sent_time,
				'message_from': message.message_from.username
			})

		for room_user in users:
			print(room_user)
			users_parsed.append(room_user.user.username)

		return {
			'name': room.name.replace(".", "_"),
			'room_id': room.room_id,
			'owner': room.owner.username,
			'messages': msg_parsed,
			'users': users_parsed
		}


	""" Convert stored string of nft addresses to list and return to user """
	def whiteListedArray(data):
		new_data = []
		if len(data) > 0:
			new_data = data.split(',')
		return new_data


	""" Add NFT address to whitelist array """
	def addToWhitelist(data, new_value):
		if len(data) == 0:
			return new_value

		l = data.split(',')
		if new_value not in l:
			l.append(new_value)

		return ','.join(l)



	""" Remove NFT address from whitelist array """
	def removeFromWhitelist(data, item):
		l = data.split(',')
		l.remove(item)
		new_data = ','.join(l)
		return new_data
