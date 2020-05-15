from flask import Flask, redirect, flash, render_template, request, url_for, session, g
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from forms.forms import newSkater, search, loginForm, contactForm, registration
from flask_wtf.csrf import CSRFProtect, CSRFError
import os
import json
import random
import sqlite3


data=[]
	
with open('static/skaters.json') as f:
	data = json.load(f)
	f.close()


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
bcrypt = Bcrypt(app)
mongo = PyMongo(app)
csrf = CSRFProtect(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html") 

@app.before_request
def before_request():
        g.username = None
        if 'username' in session:
                g.username = session['username']

@app.route("/test")
def home_page():
    online_users = mongo.db.users.find({"online": True})
    return render_template("mongo.html",
        online_users=online_users)


@app.route('/')
@app.route('/home')
def home():
	if g.username:
		return render_template("index.html", loggedIn= "yes", username=g.username)

	else:
		return render_template("index.html")




@app.route('/Search/', methods=['POST', 'GET'])
def my_form_post():
	if request.method == 'POST':
		print ("request form")
		search = request.form['search']
			
		for  skater in data:
		
			print("Value: " + str(skater))
			if search in skater:
				skater=skater[search]
				print ("this worked")	
				  
			else:
				return("There are no results for your search, try again.")
				print ("DOES NOT WORK")
	
		return render_template("Search.html", search=search, skater=skater)

@app.route('/contact/', methods=['POST', 'GET'])
def contact():
	form = newSkater(request.form)
	contactform = contactForm(request.form)
	return render_template("contact.html", form=form, contactForm=contactform)


@app.route('/brand/<string:stat>')
def brand(stat):
	txt_url=open('static/' + stat + '.txt') 
	content = txt_url.read()
	txt_url.close()
	img_url = url_for('static', filename= stat+'.jpg')
	return render_template("brand.html", img_url=img_url, txt_url=content, stat=stat)

@app.route('/list/<stat>')
def lists(stat):

	return render_template("results.html")

@app.route('/upload/', methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		print ("request.form")
		upload = request.form['upload']
		with open('static/newSkaters.json', 'w') as G:
			json.dump(request.form, G)
		return render_template("upload.html", upload=upload)

@app.route('/Login/', methods=['GET', 'POST'])
def LogIn():
        form = loginForm(request.form)       
        if request.method == 'POST':  
                conn = sqlite3.connect('library.db')                
                with conn:
                        c = conn.cursor()
                        try:
                                find_user = ("SELECT * FROM users WHERE username = ?")
                                c.execute(find_user, [(form.username.data)])
                                results =c.fetchall()                        
                                userResults = results[0]
                                if bcrypt.check_password_hash(userResults[1],(form.password.data)):
                                        session['username'] = (form.username.data)
                                        return redirect(url_for('home'))
                                else:
                                        flash('Either username or password was not recognised')
                                        return render_template('login.html', form=form)   
                        except Exception as e:print(e)

                        flash('Either username or password was not recognised')
                        return render_template('login.html', form=form)                                 
        return render_template("login.html", form=form) 

@app.route("/logout")
def logout():        
        session['logged_in'] = True
        session.clear()
        flash("You have successfully logged out.")
        return redirect('home')


@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def SignUp():
        if g.username:
                return redirect('home')
        else:
                registerForm = registration(request.form) 
                if request.method == 'POST':
                        pw_hash =bcrypt.generate_password_hash(registerForm.password.data)
                        newEntry = [((registerForm.username.data), pw_hash, (registerForm.emailAddress.data), 'No')]

                        conn =sqlite3.connect('library.db')
                        print ("Opened database successfully")
                        with conn:
                                c =conn.cursor()
                                try:
                                        signupSQL = '''INSERT INTO users (username, password, email, admin) VALUES(?,?,?,?)'''
                                        c.executemany(signupSQL, newEntry)
                                        print ("Insert correctly")
                                except:
                                        flash("This is already an account, please log in with those details or change details.")
                                        c.commit()
                                        return render_template("signup.html", form=registerForm)
                                flash((registerForm.username.data) + " Successfully Registered!")
                                session['logged_in'] = True
                                session['username'] = (registerForm.username.data)
                                return redirect('account')                                
                        return render_template("signup.html", form=registerForm)
                return render_template('signup.html', form=registerForm)
		 
if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)