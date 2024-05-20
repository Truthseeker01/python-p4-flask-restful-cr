#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):

    def get(self):
        # response_dict = {
        #     "message": "Welcome to the Newsletter RESTful API",
        # }
        # response = make_response(
        #     response_dict, 200
        # )
        # return response
        return {"message": "Welcome to the Newsletter RESTful API"}, 200
    
api.add_resource(Home, '/')

class Item(Resource):

    def get(self):

        return {
            "item1": "tea",
            "item2": "tea2",
            "item3": "tea3",
            "item4": "tea4"
        }, 200

api.add_resource(Item, '/items')

class Newsletters(Resource):

    def get(self):

        return [n.to_dict() for n in Newsletter.query.all()], 200
    
    def post(self):
        new_record = Newsletter(
            title=request.json['title'],
            body=request.json['body']
        )

        db.session.add(new_record)
        db.session.commit()

        return new_record.to_dict(), 201
    
api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):

    def get(self, id):
        n = Newsletter.query.where(Newsletter.id == id).first()
        return n.to_dict(), 200
    
api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
