from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from passlib.hash import sha256_crypt

#file imports
from routes import app
from routes import db

@app.route('/register', methods = ['GET', 'POST'])	
def register():
	#form = RegisterForm(request.form)
	if request.method == 'POST':
		#fetch form data
		firstname = request.form['first_name']
		lastname = request.form['last_name']
		username = request.form['user_name']
		password = sha256_crypt.encrypt(str(request.form['password']))

		user = User(firstname, lastname, username, password)
		db.session.add(user)
		db.session.commit()

		flash('You have been registered', 'success')
		return redirect(url_for('index'))
	return render_template('register.html')	
#View all users
@app.route('/users')
def users():

	#View all users
	return render_template('users.html', users = User.query.all() )

#View a single user

@app.route('/user/<string:id>/')	
def user(id):
	return render_template('user.html', user = User.query.get(id))

#Delete a user

@app.route('/deleteuser', methods = ['POST', 'GET'])
def delete_user():
	if request.method =='POST':
		username = request.form['user_name']
		user = User.query.filter_by(username = username).first()
		db.session.delete(user)
		db.session.commit()

		flash('The user has been deleted!', 'danger')
		return redirect(url_for('index'))
	return render_template('deleteuser.html')

#Update  username

@app.route('/updateuser', methods = ['POST', 'GET'])
def update_user():
	if request.method == 'POST':
		username_current = request.form['user_name']
		new_username = request.form['new_name']
		user = User.query.filter_by(username = username_current).first()
		user.username = new_username

		db.session.commit()
		flash('Username updated!', 'success')
		return redirect(url_for('index'))
	return render_template('updateuser.html')