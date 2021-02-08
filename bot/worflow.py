import secrets
import uuid

# public libs 
from flask import Flask, request, jsonify

# local 
from utils.bot import Bot
from utils.model_handler import ModelHandler
from utils.similarity_mesure import SimilarityMesure


# cretae a new app 
app = Flask(__name__)
app.secret_key=secrets.token_urlsafe(16)
app.config['APPLICATION_ROOT'] = '/api/conversation'
app.config['SYSTEM_FILE_STORAGE'] = 'storage.json'

# create a mesure unit with threash hold greater then 70  
SimMes = SimilarityMesure(threash = 0.7)

# create a workflow manager
bot = Bot(app.config['SYSTEM_FILE_STORAGE'], SimMes)

# load model data 
model = ModelHandler("../kindly-bot.json")
# load data into memory 
bot_memory = model.read_model()


@app.route('/api/conversation/start', methods=['POST', 'GET'])
def start():
	# used to get user history , if exist 
	if request.method == 'GET':
		if 'user_id' in request.json:
			re = bot.getter(request.json['user_id'])
			if re:
				return jsonify(message=f'your conversation history is : {re}'), 200
			return jsonify(message=f"the provided user_id : {request.json['user_id']} has not history"), 404

	if request.method == 'POST':
		# check if user already set
		if 'user_id' in request.json:
			return jsonify(message='Language already set, go to message !!! '), 200
		# validate language 
		language_ = bot.validate_language(request.json)
		if not language_['status'] :
			return language_['reason'], 404
		# set language
		user_id = bot.set_language(language_['reason'])

		# make a rondom greeting response   
		re = bot.greeting_fallback_handler(memory = bot_memory,
								language=language_['reason'],
								dialog_type = 'greetings')
		
		return jsonify(user_id = user_id, message=re), 200

	return jsonify(message="Method most be oneof ['POST', 'GET']"), 400



@app.route('/api/conversation/message', methods=['POST'])
def message():
	if request.method == 'POST':
		if 'user_id' not in request.json:
			return jsonify(message='please use /url to setup language and persid to conversation'), 404
		
		user_id = request.json['user_id']
		# check if paylod contain a message 
		if 'message' in request.json:

			# get language
			user_stored_data = bot.getter(user_id)
			if 'language' not in user_stored_data:
				return jsonify(user_id = user_id,message=f"user with id = {user_id} has no language set, please use /api/conversation/start to set the language"), 404
			lang = user_stored_data['language']

			sample = bot.conversation_handler(message = request.json['message'],
										memory = bot_memory,
										language = lang,
										dialog_type = "SAMPLES" )
			if not sample :
				 keyword = bot.conversation_handler(message = request.json['message'],
										memory = bot_memory,
										language = lang,
										dialog_type = "KEYWORDS" )
			if not keyword : 
				fallback = greeting_fallback_handler(memory = bot_memory,
								language=language_['reason'],
								dialog_type = 'fallback')
				return jsonify(user_id = user_id, message=fallback), 200
			return jsonify(message=response.encode('utf-8')), 200
		return jsonify(message = "Please check your json payload, message was not found !! "), 404






