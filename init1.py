#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='PriCoSha',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	fname = request.form['fname']
	lname = request.form['lname']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s, %s, %s)'
		cursor.execute(ins, (username, password, fname, lname))
		conn.commit()
		cursor.close()
		return render_template('home.html')

@app.route('/home')
def home():
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT name, description FROM FriendGroup WHERE username = %s'
    cursor.execute(query, (username))
    data2 = cursor.fetchall()
    query = 'SELECT ID, timestamp, name, link, privacy FROM Content WHERE username = %s ORDER BY timestamp DESC'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('home.html', username=username, posts=data, friendgroups=data2) 
		
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	name = request.form['name']
	link = request.form['link']
	privacy = request.form['privacy']r
	id = int(request.form['id'])
	query = 'INSERT INTO Content (name, link, privacy, username,id ) VALUES(%s, %s, %s, %s, %s)'
	cursor.execute(query, (name, link, privacy, username, id))
	
	if privacy == "private":
		friendgroups = request.form['friends']
		query = 'INSERT INTO Share (name, ID, owner) VALUES (%s, %s, %s)'
		cursor.execute(query,( friendgroups, id, username))
		
	query = 'INSERT INTO Post (username, id) VALUES (%s, %s)'
	cursor.execute (query, (username, id))

	conn.commit()
	cursor.close()
	return redirect(url_for('home'))
	
@app.route('/addfg', methods=['GET', 'POST'])
def addfg():
    username = session['username']
    cursor = conn.cursor()
    name = request.form['name']
    description = request.form['description']
    query = 'INSERT INTO FriendGroup (name, description, username) VALUES (%s, %s, %s)'
    cursor.execute(query, (name, description, username))   
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))
	
@app.route('/addtofg', methods=['GET', 'POST'])
def addtofg():
	username = session['username']
	cursor = conn.cursor()
	name = request.form['name']
	friendgroup = request.form['friendgroups']
	query = 'INSERT INTO member_of (username, name, owner) VALUES (%s, %s, %s)'
	cursor.execute (query, (name, friendgroup, username)) 
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))
    
@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
