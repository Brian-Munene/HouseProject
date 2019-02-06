from flask import Flask, session, logging, request, json, jsonify
from passlib.hash import sha256_crypt

#file imports
from routes import app
from routes import db
from database.user import User

@app.route('/register', methods = ['GET', 'POST'])	
def register():
	#form = RegisterForm(request.form)
	if request.method == 'POST':
		request_json = request.get_json()

		firstname = request_json.get('firstname')
		lastname = request_json.get('lastname')
		username = request_json.get('username')
		password = sha256_crypt.encrypt(str(request_json.get('password')))
		category = request_json.get('category')

		user = User(firstname, lastname, username, password, category)
		db.session.add(user)
		db.session.commit()

		return('You have been registered', 'success')
	return ('Invalid Method')	
#View all users
@app.route('/users')
def users():
	users = User.query.all()

	usersList = []
	for user in users:
		users_dict = {
				'firstname': user.firstname,
				'lastname': user.lastname,
				'username': user.username,
				'category': user.category
				}
		usersList.append(users_dict)
	return jsonify({'data' :usersList})
	

#View a single user

@app.route('/user/<string:id>/')	
def user(id):
	user = User.query.get(id)
	user_dict = {
				'firstname': user.firstname,
				'lastname': user.lastname,
				'username': user.username,
				'category':user.category
				}
	return jsonify({'data' :user_dict})

#Delete a user

@app.route('/deleteuser', methods = ['POST', 'GET'])
def delete_user():
	if request.method =='POST':
		request_json = request.get_json()
		username = request_json.get('username')
		user = User.query.filter_by(username = username).first()
		db.session.delete(user)
		db.session.commit()

		return('The user has been deleted!', 'success')
	return ('Invalid Method')

#Update  username

@app.route('/updateuser', methods = ['POST', 'GET'])
def update_user():
	if request.method == 'POST':
		request_json = request.get_json()

		username_current = request_json.get('username')
		new_username = request_json.get('new_name')
		user = User.query.filter_by(username = username_current).first()
		user.username = new_username

		db.session.commit()
		return('Username updated!', 'success')
	return ('Invalid Method')

@app.route('/SingleCategoryUser/<string:category>/')
def single_category_user(category):
	users = User.query.filter_by(category = category)
	usersList = []
	for user in users:
		users_dict = {
				'firstname': user.firstname,
				'lastname': user.lastname,
				'username': user.username,
				'category': user.category
				}
		usersList.append(users_dict)
	return jsonify({'data' :usersList}) 
