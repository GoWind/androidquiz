import pymongo
from androidquiz import coll_counter , coll_questions , coll_users , coll_submitted_users,cache
import datetime
from uuid import uuid4
import json
import pymongo
def has_submitted(teamid):
		team  = coll_submitted_users.find_one({'_id':str(teamid)})
		return team is  not  None

def update_seq_by1(collection,id):
		'''updates the sequence number of selected collection by one ( eg. increase no of users by one)'''
		collection.find_and_modify(   query = { "_id" : id} , update = { "$inc" : { "seq" : 1} } , upsert=True )

def get_seq(collection , id):
		y= collection.find_one({ "_id" : id })
		if y:
			return int(y['seq'])
		return None    


def search_for_team(teamname,password):
	team = coll_users.find_one({'teamname': teamname , 'password':password})
	return team

def submit_team(teamid ,teamname,answers):
	'''questions is a dict with keys forming question numbers and values as answers'''
	coll_submitted_users.insert({"_id" :teamid, "teamname":teamname, "submitted_answers" : answers , "submitted" : True})
		

def add_team(email,contact_no,name_1,name_2,institution):
	''' adding a team by manager'''
	currentno = get_seq(coll_counter,"users")
	teamname = "droidsfida" + str(currentno)
	password = str(uuid4())[:7]
	try:
	  coll_users.insert( { "_id" : currentno , "teamname" : teamname ,'registered':False,'password': password,
		                 'email':email,'contact_no':contact_no,'name_1':name_1,'institution':institution,'name_2':name_2})
	  update_seq_by1(coll_counter , "users")
	except pymongo.errors.PyMongoError:
		return ("Error","Unable to add user")
	return (teamname,password)



def search_for_unregistered_team(teamname):
	'''returns a document identifying if a team is registerted'''
	team_doc = coll_users.find_one({'teamname':teamname,'registered' :False })
	return team_doc

def search_for_registered_team(teamname,password):
	team_doc = coll_users.find_one({'teamname':teamname , 'registered':True,'password':password })
	return team_doc



def add_question(question_text , options , answer,answer_type):
	''' add question '''
	currentno = get_seq(coll_counter,"questions")
	coll_questions.insert({"_id":str(currentno),"question_text":question_text,"options":options,"answer":answer, "type":answer_type})
	update_seq_by1(coll_counter , "questions")
	

def register_team(teamid,password):
	'''registers a team by setting registered field to true and then setting its password'''
	coll_users.update({'_id' : int(teamid) } , { '$set' : { 'registered' : True ,'password' : password } })
	return True
	
	
''' will need to modify this to generate random questions . '''
def get_questions():
	questions = []
	q = coll_questions.find()
	for quest in q:
		questions.append(quest)
	return questions


def get_results(teamid):
	answers = coll_submitted_users.find_one({'_id' : teamid })
	if answers:
		return answers['submitted_answers']
	return None


def calculate_score(submitted_answers):
	answers = cache.get('questions')
	if answers is None:
	   answers = get_question_dict()
	count = 0
	for answer in submitted_answers:
		if answer in answers and answers[answer] == submitted_answers[answer]:
			count += 1
	return count

def get_question_dict():
	   answers =dict()
	   cursor = coll_questions.find()	
	   for doc in cursor:
		answers[str(doc['_id'])] = doc["answer"]
	   return answers

def get_team_doc(teamid):
	doc = coll_users.find_one({"_id":int(teamid)})
	if not doc:
		return None
	return doc
