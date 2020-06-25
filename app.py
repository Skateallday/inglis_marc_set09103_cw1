from flask import Flask, redirect, flash, render_template, request, url_for, session, g
import os
import json
import random


data=[]
	


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html") 


@app.route('/')
@app.route('/home')
def home():
		return render_template("index.html")


@app.route('/dash')
def dash():
	return render_template("dash.html")

@app.route('/store')
def store():
		return render_template("store.html")


@app.route('/soldout')
def soldout():
		return render_template("soldout.html")

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
