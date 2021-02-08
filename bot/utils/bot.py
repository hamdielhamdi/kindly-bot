import secrets
import json
import os 

class Bot:
	def __init__(self,storage_name,SimMes ):
		self.SimMes = SimMes
		self.storage_name = storage_name
		self.touch_if_not_exist()
		self.check_storage()

	def validate_language(self,arg):
			# check if language is set 
			if 'language' in arg:
				if arg['language']  in ['en', 'nb']:
					return {'status' : True, 'reason': arg['language']}
				return {'status' : False, 'reason': 'language most be onefo [en, nb] !! '}
			return {'status' : False, 'reason': 'a query language most be defined in the http requests level !! '}


	def access_file(self, mode = 'r'):
		# access file and return file object 
		return open(self.storage_name, mode)

	def touch_if_not_exist(self):
		# create file if not exist 
		if not os.path.exists(self.storage_name):
			open(self.storage_name, 'a')

	def check_storage(self):
		
		content = self.access_file(mode = 'r+')
		# initiate file with min dict 
		if 'users' not in content.read() : 
			init = {"users":[]}
			content.seek(0)
			content.write(str(init))

	 
	def set_language(self, language):
		# will append new user as {'user_id': int, 'language':'en/dn', 'action':{}} 
		content = self.access_file(mode = 'r+')
		rows = eval(content.read())
		payload_new_user = {'user_id':(len(rows['users']) + 1), 'language':language, 'action':{}}
		rows['users'].append(payload_new_user)
		content.seek(0)
		content.write(str(rows))
		return payload_new_user['user_id']

	def make_choice(self, list_of_choice):
		# make  a rondom choice from a list of items 
		if len(list_of_choice) > 0:
			return secrets.choice(list_of_choice)
		return None 

	# O(n) complexity 
	def getter(self, key):
		# get user schema from session storage
		found = False
		content = self.access_file(mode = 'r+')
		rows = eval(content.read())
		for user in rows['users']: 
			if user['user_id'] == key:
				found = True
				return user
		return (user if found else found)

	def greeting_handler(self, memory, language, dialog_type):
		# valid for greeting and fallback
		conversation_data = memory[dialog_type][0]
		replies = conversation_data['replies'][language]
		return  self.make_choice(replies)

	# can be replaced with str.lower() since the key is allways dialogeu_type.lower 
	# but for the clarity of the code will keep it ;)
	def mapper_(self, key):
		mapper = {"SAMPLES":"samples","KEYWORDS":"keywords"}
		return mapper[key]


	# O(n*m) : n: nbr dialogues, m : nbr samples by dialogs
	# O(n*m) ~ O(n) since m is too smole compare to n,
	# but can be better with reshaped data structure or like a binary shearch algo
	# time complexity can be n*log(n) 
	def conversation_handler(self,message, memory, language, dialog_type):
		possible_replies = []
		# this will iter thru all samples /keywaors base on dialog_type
		for dict_ in memory['dialogues']:
			# check dialogue_type = dialog_type selected oneof [SAMPLES, keywords]
			if dict_['dialogue_type'] == dialog_type:
				# access base-on language key oneof [saples, keywords] 
				key = self.mapper_(dialog_type)
				list_items = dict_[key][language]
				# performe mesure 
				result  = self.SimMes.mesure_sim(message, list_items)
				# filter None
				if result:
					# pickup a rondom response and memorize it 
					result.update({'reply':self.make_choice(dict_['replies'][language])})
					possible_replies.append(result)
		print(possible_replies)
		# if we have possible condidate from samples first, return romdom  response
		if len(possible_replies)> 0:
			return self.SimMes.sort_list_dict(possible_replies, 'mesure')[0]['reply']
		return None
		
