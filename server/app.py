#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    
    def get(self):
        all_plants = [plant.to_dict() for plant in Plant.query.all()]
        response = make_response(
            jsonify(all_plants), 
            200
        )

        return response
    
    def post(self):
        request_json = request.get_json()
        new_plant = Plant(
            name=request_json['name'],
            image=request_json['image'],
            price=request_json['price'],    
        )

        db.session.add(new_plant)
        db.session.commit()

        response = make_response(
            jsonify(new_plant.to_dict()),
            201
        )

        return response


api.add_resource(Plants, '/plants',)


class PlantByID(Resource):
    
    def get(self, id): 
        found = Plant.query.filter_by(id=id).first().to_dict()
        response = make_response(
            jsonify(found),
            200
        )

        return response
    
api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
