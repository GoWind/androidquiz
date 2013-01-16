from androidquiz import app,roles
from models import add_question
from flask import request , Response ,session,redirect, url_for,render_template
from cgi import escape
from functools import wraps


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
@app.route('/submitquestion',methods=['POST'])
@requires_auth
def submitquestion():
	if request.method == 'POST':
			options = {}
			question_text = request.form['questiontext']
			options['a'] = request.form['optiona']
			options['b'] = request.form['optionb']
			options['c'] = request.form['optionc']
			options['d'] = request.form['optiond']
			answer = request.form['answer']
			type= request.form['type']
			add_question(question_text,options,answer,type)
				
			return "operation successfully done"
	return "GET not supported"		


