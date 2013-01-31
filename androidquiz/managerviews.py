from androidquiz import app,roles,coll_submitted_users,coll_questions
from models import add_question , add_team,calculate_score,get_team_doc
from flask import request , Response ,session,redirect, url_for,render_template
from cgi import escape
from functools import wraps
import operator

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 404,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

	

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
		if not 'logged_in_as' in session :
					return authenticate()
		if session['logged_in_as'] != roles[1]:
					return authenticate()
		return f(*args, **kwargs)
    return decorated
	
	
	


manpage = ''' <html> <head> <title>Manager Login</title></head>
				<body>
					<form method="POST" action="">
						Username <input type="text" name="username"/>
						Password <input type="password" name="password"/>
						<input type="submit" value="login"/>
					</form>
				</body>
			 </html>
		'''

	
	
@app.route('/managerlogin',methods=['GET','POST'])
def managerlogin():
	''' page for manager login'''
	if request.method == 'POST':
		y = escape(request.form['password'])
		if y == 'bingochips':
			session['logged_in_as']=roles[1]
			session['logged']=True
			session.permanent = False
			return redirect(url_for('managerhome'))
	return manpage


@app.route('/managerhome')
@requires_auth
def managerhome():
	'''homepage for manager'''
	return render_template('managerhome.html')

@app.route('/managerlogout')
def managerlogout():
	''' logout manager '''
	session.pop('logged_in_as',None)
	session.pop('logged',None)
	return "Logged out"



	
''' add question'''
@app.route('/submitquestion',methods=['GET','POST'])
def submitquestion():
	if 'logged_in_as' not in session or session['logged_in_as'] != roles[1]:
		return Response("Illegal Access",403)
	if request.method == 'POST':
			options = {}
			question_text = request.form['questiontext']
			options['a'] = request.form['optiona']
			options['b'] = request.form['optionb']
			options['c'] = request.form['optionc']
			options['d'] = request.form['optiond']
			answer = request.form['answer']
			qtype="single"
			add_question(question_text,options,answer,qtype)
				
			return "operation successfully done"
	return render_template("submit_question.html")		



@app.route('/addteam',methods=['GET','POST'])
@requires_auth
def addteam():
	if request.method == 'POST':
		email = request.form['email']
		contact_no = request.form['contact_no']
		institution = request.form['institution']
		name_1 = request.form['name_1']
		team_data = add_team(email,contact_no,name_1,institution)
		return "teamname:%s password %s"%(team_data[0],team_data[1])
	return "Operation not possible.Try again"
	


@app.route('/current_results')
@requires_auth
def get_current_results():
	list_of_scores = dict()
	submitted_users = coll_submitted_users.find()
	for user in submitted_users:
		teamid = user['_id']
		teamdoc = get_team_doc(teamid)
		score = calculate_score(user['submitted_answers'])
		list_of_scores[teamid] = [teamdoc['teamname'],teamdoc['institution'],teamdoc['contact_no'],score]
	return render_template('results.html',scores=list_of_scores,title="Results")

@app.route('/allquestions')
@requires_auth
def allquestions():
	questions = coll_questions.find()
  	l = []
	for question in questions :
		l.append(question)
	return render_template('questions.html',questions=l)
	
