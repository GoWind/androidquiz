import sys
from flask import Flask
import pymongo
app = Flask(__name__)

app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017
app.config['MONGODB_DATABASE'] = __name__
app.config['SECRET_KEY'] =  "Bingofromhell!@#$%^&*SDFASFSR#$%^$%^TGRERWEREWRWRWERWQRWER$^&*&*^YUJJK"
database = 'androidquiz'

'''configuration for database '''
''' following shows collection names in the database . Names are self descriptive '''

counter = 'counter'
users  = 'users'
questions = 'questions'
submitted_users = 'submitted_users'

roles = ["user","manager","admin"]


''' init connection to database'''
try:
	datastore = pymongo.MongoClient()
except pymongo.ConnectionFailure:
	print "Problem in connection to database. Application is exiting"
	sys.exit(1)


	
'''init collections. Will be used by models to update stuff ''' 
coll_counter = datastore[database][counter]
coll_users = datastore[database][users]
coll_questions = datastore[database][questions]
coll_submitted_users = datastore[database][submitted_users]



''' initialize counter by hand as I havent really found a nice way to initialize it programatically'''
qcounter = coll_counter.find_one({"_id": "questions"})
if not qcounter:
			coll_counter.insert({"_id": "questions" , "seq":0})
ucounter = coll_counter.find_one({"_id": "users"})
if not ucounter:
			coll_counter.insert({"_id": "users" , "seq":0})
sucounter = coll_counter.find_one({"_id": "submitted_users"})
if not sucounter:
			coll_counter.insert({"_id": "submitted_users" , "seq":0})



import androidquiz.views
import androidquiz.managerviews
