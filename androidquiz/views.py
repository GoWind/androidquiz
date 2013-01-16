from androidquiz import app,roles, coll_users
from flask import render_template,url_for,redirect,request,flash,session,Response
from cgi import escape
import models
from functools import wraps


def authenticate():
	return Response('Sorry . you need to login to see the page',404)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
		if not 'logged_in_as' in session :
					return authenticate()
		if session['logged_in_as'] != roles[0] or 'teamid' not in session:
					return authenticate()
		return f(*args, **kwargs)
    return decorated



@app.route('/',methods=['GET','POST'])

def home():
	''' view for homepage'''
	if request.method == 'POST':
		teamname = escape(request.form['teamname'])
		team = models.search_for_team(teamname)
		if not team:
			return "error . your team isnt found . Please ask for a teamname from the event organizers"
		else:
			return render_template('registerteam.html',team=team)
	return render_template('home.html')


 
@app.route('/registerteam', methods=['GET','POST'])
def register_user():
	'''registers a team and enable them to access the quiz '''
	if request.method == 'POST':
	  	teamid = escape(request.form['id'])
	  	password = escape(request.form['password'])
	  	confirm = escape(request.form['confirm'])
	  	if confirm != password:
	  			return "passwords dont match enter again"
	  	else:
		 '''register team'''
		 result = models.register_team(teamid,password)
		 if not result:
			return "An error has occured.Please try again later"
		 else:
			return "You have registered successful.Login from the homepage to access the quiz"

		
	

	
@app.route('/quiz',methods=['GET','POST'])
@requires_auth
def quiz():	
	if models.has_submitted(session['teamid']):
		return "You have already taken the quiz. You cannot take it again"
	questions = models.get_questions()
	return render_template('quizpage.html',questions = questions,teamid=session['teamid'])


@app.route('/submit',methods=['GET','POST'])
@requires_auth
def submit():
		if request.method == 'POST':
			team_answers = dict()
			teamid =''
			for key in request.form:
				if key == 'teamid':
					teamid = request.form[key]
				else:
					team_answers[key] = request.form[key]
			if len(teamid) == 0:
				return "Error in submitting form"
			models.submit_team(teamid,team_answers)
			return "You have submitted your response  . Please wait until we announce the results"
		return "Get not supported"



@app.route('/loginteam',methods=['GET','POST'])
def loginteam():
	'''logs in checked and registered teams'''
	'''check to see if user has already submitted his quiz'''
	if request.method == 'POST':
		teamnumber = escape(request.form['teamnumber'])
		password = escape(request.form['password'])
		y = models.search_for_registered_team(teamnumber,password)
		if y:
		 session['teamid']=teamnumber
		 session['logged_in_as'] = roles[0]
		 session['logged'] = True
		 session.permanent = False
		 '''replace it with landing'''
		 return redirect(url_for('quiz'))
		else:
			return "Sorry . Not allowed"
	return render_template('loginteam.html')



