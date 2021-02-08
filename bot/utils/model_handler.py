import json 
import os 
"""
The mean use of ModelHandler class is to : 
1 - read the model file's from the 'kindly-bot.json'.
2 - load in memory
"""
class ModelHandler: 
	def __init__(self, source_file):
		self.source_file = source_file

	def read_model(self):
		"""
		reason :
			 read the json file 
		Attributes: 
			source_file : json model 
		return:  
			None
		""" 
		with open(self.source_file) as json_file:
			model = json.load(json_file)
		return model

