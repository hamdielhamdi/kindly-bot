import unittest

import sys, os, json
sys.path.append('../')

from utils.model_handler import ModelHandler 
from utils.bot import Bot 
from utils.similarity_mesure import SimilarityMesure 


class MainTestCase(unittest.TestCase):
	def setUp(self):
		self.content = ModelHandler('content.json').read_model()
		self.ms = SimilarityMesure(0.7)
		self.bot = Bot('tmp.json', self.ms) 
		

	# read data source
	def test_c_model(self):
		self.assertIsInstance(self.content, dict)
		self.assertTrue(os.stat('content.json').st_size>0)

	# set language and access file
	def test_bot(self):
		self.assertAlmostEqual(self.bot.set_language('en'), 1)
		test_data = {'users': [{'user_id': 1, 'language': 'en', 'action': {}}]}
		self.assertAlmostEqual(eval(self.bot.access_file().read()),test_data)
	# make choice
	def test_choice(self):
		self.assertFalse(self.bot.make_choice([]))
		self.assertTrue(self.bot.make_choice([1,2]))

	# get data by key 
	def test_getter(self):
		self.assertFalse(self.bot.getter(1))

	# make conversation 
	def test_conversation_handler(self):
		result = self.bot.conversation_handler(message = 'Do you know the meaning of kindness?',
												memory = self.content,
												language='en',
												dialog_type = 'SAMPLES')
		self.assertIsNotNone(result)

	# delete tmp file 
	def tearDown(self):
		os.remove('tmp.json')
	
if __name__ == '__main__':
	unittest.main()