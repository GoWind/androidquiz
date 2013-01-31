from androidquiz import app,roles, coll_users,cache
from flask import render_template,url_for,redirect,request,flash,session,Response
from cgi import escape
import models
from functools import wraps
import pymongo


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
	return redirect(url_for('loginteam'))

 

		
	

	
@app.route('/quiz',methods=['GET','POST'])
@requires_auth
def quiz():	
	if models.has_submitted(session['teamid']):
		return render_template('errorpage.html',error_header="Oopsie!",error_message="It Looks like you have already taken your quiz.<a href='/logout'>Click here to logout</a>")
	if 'quizac' not in session:
		session['quizac'] = 1
		questions = models.get_questions()
		return render_template('quizpage.html',questions = questions,teamid=session['teamid'],teamname = session['teamname'])
	elif session['quizac'] == 1:
		return render_template('errorpage.html',error_header="Oops !",error_message="Sorry.But page reloads aint allowed.Contact the event co-ordinator")
	


@app.route('/submit',methods=['GET','POST'])
@requires_auth
def submit():
		if request.method == 'POST':
			if models.has_submitted(session['teamid']):
				return "You have already submitted  your quiz."
			team_answers = dict()
			if 'teamid' not in request.form :
				return "Error in submitting form"
			teamid =''
			teamid = request.form['teamid'].strip()
			for key in request.form:
				if key == 'teamid':
					continue
				else:
				   team_answers[str(key).strip()] = request.form[key].strip()
			models.submit_team(teamid,session['teamname'],team_answers)		        			
			return "Your response has been submitted . Please wait for a short period of time till we announce the results"

		return "Get not supported"



@app.route('/loginteam',methods=['GET','POST'])
def loginteam():
	'''logs in checked and registered teams'''
	'''check to see if user has already submitted his quiz'''
	if request.method == 'POST':
		teamnumber = escape(request.form['teamname'])
		password = escape(request.form['password'])
		y = models.search_for_registered_team(teamnumber,password)
		if y:
			teamid = y['_id']
			if models.has_submitted(teamid):
			  return render_template('errorpage.html',error_header="Oopise !",error_message="Sorry. You have already taken the quiz. You cant take it again")
			session['teamid']=y['_id']
			session['teamname'] = teamnumber
			session['logged_in_as'] = roles[0]
			session['logged'] = True
			session.permanent = False
			return redirect(url_for('quiz'))
		else:
			return render_template('errorpage.html',error_header="Invalid", error_message='Either your username or password is invalid.Check again')
	return render_template('loginteam.html')


@app.route('/logout')
@requires_auth
def logout():
	for key in ['teamid','teamname','logged_in_as','logged' ]:
		session.pop(key,None)
	return "Thank you we will post the result of the quiz in a short span of time"



@app.route('/error')
def error():
	return render_template('errorpage.html',error_header="Sample Error",error_message="Dai error da")




		
