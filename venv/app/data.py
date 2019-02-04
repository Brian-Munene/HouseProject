def Houses():
	houses = [
		{
			'id': 1,
			'type': 'Single-Room',
			'price': 12000,
			'owner': 'Brian'
		},
		{
			'id': 2,
			'type': 'Double-Room',
			'price': 15000,
			'owner': 'Patrick'
		},
		{
			'id': 3,
			'type': 'Single',
			'price': 12000,
			'owner': 'Lydia'
		},
	]

	return houses

def Users():
	users = [
		{
			'id': 1,
			'fname': 'Brian',
			'lname': 'Munene',
			'uname': 'Brayo'
		},
		{
			'id': 2,
			'fname': 'Ian',
			'lname': 'Nene',
			'uname': 'Ian'
		},
		{
			'id': 3,
			'fname': 'Geoffrey',
			'lname': 'Munguti',
			'uname': 'Jeff'
		},
	]

	return users

def Rentals():
	rentals = [
		{
			'id': 1,
			'tenant': 'Brayo',
			'amount': 12000,
			'date': '1 February 2019',
		},
		{
			'id': 2,
			'tenant': 'Ian',
			'amount': 11000,
			'date': '2 February 2019'
		},
		{
			'id': 3,
			'tenant': 'Jeff',
			'amount': 10000,
			'date': '30 January 2019'
		},
	]
	return rentals
