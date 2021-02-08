# KINDLY-BOT

kINDLY-BOT is a simple chat bot to handle simple conversation, it's implemented based on Flask framework. 
## Assumption
* No use of cookie to follow the incoming requests, instead use the user_id. 
* The NLP implemented module is a basic workflow for text processing and measuring similarity.
* Flask is the web framework.
* The project structure is defined as following, overview: 

```
kindly-bot
	|
	bot
		|-->test  : test folder 
		|-->utils : contain all necessary class (data processing)
		|		|-->bot.py(where we handle the bot sessions and main workflow)
		|		|-->model_handler.py(read data source)
		|		|-->similarity_mesure.py(where we mesure text similarity)
		|-->run.py(main entry point)
		|-->workflow.py(the views and requests workflow)
		|-->storage.json(where the bot store it memory and the performed steps)
and more ...
```

* instead of using some tools like redis to store data, i used a simple local data and sessions manager, implemented from scratch.



## Installation
1  - The first of all clone the project.
```git
git clone https://github.com/hamdielhamdi/kindly-bot.git
```
2 - Access the project. 

```bash
cd kindly-bot
```
3 - Before starting, a set of requirement shloud be installed.

```bash
pip install -r requirements.txt
```
4 - Now that the requirements are installed we can run the project by following the bellow steps either as a local env or a virtual env: 

#### 4.1 run the project in a local environment :
```bash
cd bot
python run.py
```
#### 4.2 run the project in virtual environment :
```bash
# You can install the venv with pip
pip install virtualenv
source venv/bin/activate
cd bot
python run.py
```
# Usage
Set language  : 
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"language":"en"}' \
  http://localhost:5000/api/conversation/start
```
after setting language, the session manager will store the language and set a user_id , now you can proceed to the conversation : 
 
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"user_id":"1","message":"You are good at answering questions"}' \
  http://localhost:5000/api/conversation/message
```
at any time the user can get the conversation history, using the following requests : 
```
curl --header "Content-Type: application/json" \
  --request GET \
  --data '{"user_id":"1"}' \
  http://localhost:5000/api/conversation/start
```

## test
To run the tests cases  : 
```
cd kindly-bot\bot\test
python testcases.py
```
## License
[MIT](https://choosealicense.com/licenses/mit/)