import pymongo
from androidquiz import coll_counter , coll_questions , coll_users , coll_submitted_users
import datetime


def has_submitted(teamid):
		team  = coll_submitted_users.find_one({'_id':teamid})
		return team is  not  None

def update_seq_by1(collection,id):
		'''updates the sequence number of selected collection by one ( eg. increase no of users by one)'''
		collection.find_and_modify(   query = { "_id" : id} , update = { "$inc" : { "seq" : 1} } , upsert=True )

def get_seq(collection , id):
		y= collection.find_one({ "_id" : id })
		return int(y['seq']) 


def submit_team(teamid ,questions):
	'''questions is a dict with keys forming question numbers and values as answers'''
	coll_submitted_users.update({"_id" :teamid},{"$set" : { "submitted_answers" : questions , "submitted" : True } }, upsert=True)
		

def add_team(teamname):
	''' adding a team by manager'''
	currentno = get_seq(coll_counter,"users")
	coll_users.insert( { "_id" : currentno , "teamname" : teamname ,'registered':False})
	update_seq_by1(coll_counter , "users")
	return True



def search_for_unregistered_team(teamname):
	'''returns a document identifying if a team is registerted'''
	team_doc = coll_users.find_one({'teamname':teamname,'registered' :False })
	return team_doc

def search_for_registered_team(teamname,password):
	team_doc = coll_users.find_one({'teamname':teamname , 'registered':True,'password':password })
	return team_doc



def add_question(question_text , options , answer,answer_type):
	''' add question '''
	currentno = getseq(coll_counter,"questions")
	coll_questions.insert({"_id":currentno,"question_text":question_text,"options":options,"answer":answer, "type":answer_type})
	update_seq_by1(coll_counter , "questions")
	

def register_team(teamid,password):
	'''registers a team by setting registered field to true and then setting its password'''
	coll_users.update({'_id' : teamid } , { '$set' : { 'registered' : True ,'password' : password } })
	
	
''' will need to modify this to generate random questions . '''
def get_questions():
	questions = []
	q = coll_questions.find()
	for quest in q:
		questions.append(quest)
	return questions