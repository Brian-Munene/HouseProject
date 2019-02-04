from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Houses, Rentals, Users
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import pymysql.cursors

app = Flask(__name__)

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost:800'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'motongoria'
app.config['MYSQL_DB'] = 'landlord'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Initialize MySQL
mysql = MySQL(app)

#Config SQLALCHEMY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:motongoria@localhost:3306/plot'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

connection = pymysql.connect(host = 'localhost',
							user = 'root',
							password = 'motongoria',
							db = 'landlord',
							charset = 'utf8mb4',
							cursorclass = pymysql.cursors.DictCursor)
Houses = Houses()
Rentals = Rentals()
Users = Users()


#Model for the users table
class User(db.Model):
	
	__tablename__ = 'users'

	userId = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(75))
	lastname = db.Column(db.String(75))
	username = db.Column(db.String(75))
	password = db.Column(db.String(100))

	def __init__(self, firstname, lastname, username, password):
		self.firstname = firstname
		self.lastname = lastname
		self.username = username
		self.password = password

#House Model
class House(db.Model):

	__tablename__ = 'houses'

	house_id = db.Column(db.Integer, primary_key = True)
	house_number = db.Column(db.Integer)
	price = db.Column(db.Float(12))
	house_type = db.Column(db.String(20)) 

	def __init__(self, house_number, price, house_type):
		self.house_number = house_number
		self.price = price
		self.house_type = house_type

#rental Model
class Rental(db.Model):

	__tablename__ = 'rentals'

	rental_id = db.Column(db.Integer, primary_key = True)
	tenant_name = db.Column(db.String(75), unique = True)
	amount_paid = db.Column(db.Float(12))

	def __init__(self, tenant_name, amount_paid):
		self.tenant_name = tenant_name
		self.amount_paid = amount_paid

@app.route('/')
def index():
    return render_template('home.html')



#User routes for :
#Create
#Read
#Update
#Delete

#Create a User
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

#House routes for :
#Create
#Read
#Update
#Delete

#Create a House

@app.route('/InsertHouses', methods =['GET', 'POST'])
def insert_houses():
	#form = HousesForm(request.form)
	if request.method == 'POST':

		#fetch form data
		number = request.form['Number']
		price = request.form['Price']
		Type = request.form['Type']

		house = House(number, price, Type)
		db.session.add(house)
		db.session.commit()

		flash('House scuccessfully added', 'success')
		return redirect(url_for('index'))
		
	return render_template('InsertHouses.html')

#View all houses

@app.route('/houses')
def houses():
	return render_template('houses.html', houses = House.query.all() )    

#View a single house

@app.route('/house/<string:id>/')
def house(id):
	return render_template('house.html', house = House.query.get(id))  

#Update  House details

@app.route('/updatehouse', methods = ['POST', 'GET'])
def update_house():
	if request.method == 'POST':
		house_number = request.form['house_number']
		new_price = request.form['new_price']
		house = House.query.filter_by(house_number = house_number).first()
		house.price = new_price

		db.session.commit()
		flash('House Price updated!', 'success')
		return redirect(url_for('index'))
	return render_template('updatehouse.html')

#Delete a user

@app.route('/deletehouse', methods = ['POST', 'GET'])
def delete_house():
	if request.method =='POST':
		house_number = request.form['house_number']
		house = House.query.filter_by(house_number = house_number).first()
		db.session.delete(house)
		db.session.commit()

		flash('The House has been deleted!', 'danger')
		return redirect(url_for('index'))
	return render_template('deletehouse.html')


#Rental routes for :
#Create
#Read
#Update
#Delete

#Create a Rental

@app.route('/InsertRentals', methods = ['GET', 'POST'])
def insert_rentals():
	#form = RentalsForm(request.form)
	if request.method =='POST':

		#fetch form data
		tenant = request.form['tenant_user_name']
		amount = request.form['amount_paid']

		rental = Rental(tenant, amount)
		db.session.add(rental)
		db.session.commit()

		flash('Rental details successfully added', 'success')
		return redirect(url_for('index'))

	return render_template('InsertRentals.html')

#Read all rentals

@app.route('/rentals') 	
def rentals():
	return render_template('rentals.html', rentals = Rental.query.all() )

#read a single rental

@app.route('/rental/<string:tenant_name>/') 	
def rental(tenant_name):
	return render_template('rentals.html', rental = Rental.query.filter_by(tenant_name = tenant_name).first())

#Update rental
@app.route('/updaterental', methods = ['GET', 'POST'])
def update_rental():
	if request.method == 'POST':
		tenant_name = request.form['tenant_name']
		new_amount = request.form['new_amount']

		rental = Rental.query.filter_by(tenant_name = tenant_name).first()
		rental.amount_paid = new_amount

		db.session.commit()
		flash('Payment updated!', 'success')
		return redirect(url_for('index'))
	return render_template('updaterental.html')

#Delete rental
@app.route('/deleterental', methods = ['GET', 'POST'])
def delete_rental():
	if request.method == 'POST':
		tenant = request.form['tenant_name']

		rental = Rental.query.filter_by(tenant_name = tenant).first()
		db.session.delete(rental)
		db.session.commit()

		flash('Rental Details deleted!', 'success')
		return redirect(url_for('index'))
	return render_template('deleterental.html')



#Register form class handles validation and form display

'''
class RegisterForm(Form):
	first_name = StringField('First Name', [validators.DataRequired(), validators.length(min = 1, max = 35)])
	last_name = StringField('Last Name', [validators.DataRequired(), validators.length(min = 1, max = 35)])
	user_name = StringField('User Name', [validators.DataRequired(), validators.length(min = 6, max = 50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message = 'Passwords do not match!' )
		])
	confirm = PasswordField('Confirm Password', [validators.DataRequired()])
	'''


'''
class HousesForm(Form):
	Number = StringField('Number', [validators.DataRequired()])
	Price = StringField('Price', [validators.DataRequired(), validators.length(min = 3)])
	Type = StringField('House Type', [validators.DataRequired])
'''



''''
class RentalsForm(Form):
	tenant_user_name = StringField('Tenant User Name', [validators.DataRequired()])
	amount_paid = StringField('Amount Paid', [validators.DataRequired(), validators.length(min = 3)])
'''





if __name__ == "__main__":
	app.secret_key='secret123'
	app.run(debug=True)

