from flask import Flask, session, logging, request, json, jsonify

#file imports
from routes import app
from routes import db
from database.house import House
from database.house import Building

#Create a building
@app.route('/InsertBuilding', methods = ['GET', 'POST'])
def insert_building():
    if request.method == 'POST':
        request_json = request.get_json()

        name = request_json.get('Name')
        number = request_json.get('Number')
        building_type = request_json.get('building_type')

        building = Building(name, number, building_type)
        db.session.add(building)
        db.session.commit()

        return("Building successfully created", "Success")
		
@app.route('/ViewBuilding')
def view_buildings():
    buildings = Building.query.all()
    buildingList = []
    for building in buildings:
        buildings_dict = {
            'Name': building.building_name,
            'Number': building.building_number,
            'Type': building.building_type
        }
        buildingList.append(buildings_dict)
    return jsonify({'data': buildingList})

@app.route('/ViewSpecificBuilding', methods = ['GET', 'POST'])
def view_specific_building():
    if request.method == 'POST':
        request_json = request.get_json()
        number = request_json.get('Number')

        building = Building.query.filter_by(building_number = number).first()
        building_dict = {
            'Name': building.building_name,
            'Number': building.building_number,
            'Type': building.building_type
        }
        return jsonify({'data': building_dict})
    return('Method not Allowed')

@app.route('/UpdateBuilding', methods = ['POST', 'GET'])
def update_building():
    if request.method == 'POST':
        request_json = request.get_json()
        number = request_json.get('Number')
        new_name = request_json.get('new_name')
        new_type = request_json.get('new_type')
        building = Building.query.filter_by(building_number = number).first()
        
        if new_name and new_type:
            building.building_name = new_name
            db.session.flush()
            building.building_type = new_type
            db.session.commit()
            return("Building name and type have been changed", "Success")
        elif new_name:
            building.building_name = new_name
            db.session.commit()
            return ('The name has been changed', "success")
        elif new_type:
            building.building_type = new_type
            db.session.commit()
            return('The type has been changed', "Success")
    return("Method not allowed")

@app.route('/DeleteBuilding', methods=['POST'])
def delete_building():
    request_json = request.get_json()
    number = request_json.get('Number')
    building = Building.query.filter_by(building_number = number).first()
    db.session.delete(building)
    db.session.commit()
    return('Building has been deleted', 'Success')


