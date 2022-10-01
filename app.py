
from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


taskFields = {
    'id': fields.Integer,
    'name': fields.String,
    'location': fields.String
}


dataBase = {
    1: {"id": "234567",
        "name": "Cow",
        "location": "Kampala", },
    2: {"id": "26763",
        "name": "Goat",
        "location": "Jinja", },
    3: {"id": "33576",
        "name": "Sheep",
        "location": "Mubende", },

}


class Items(Resource):
    @marshal_with(taskFields)
    def get(self):
        tasks = Task.query.all()
        return tasks

    @marshal_with(taskFields)
    def post(self):
        data = request.json
        task = Task(name=data['name'], location=data['location'])
        db.session.add(task)
        db.session.commit()
        tasks = Task.query.all()
        # itemId = len(dataBase.keys()) + 1
        # dataBase[itemId] = {'id': data['id'],
        #                     'name': data['name'], 'location': data['location']}
        return tasks


class Item(Resource):
    @marshal_with(taskFields)
    def get(self, pk):
        task = Task.query.filter_by(id=pk).first()
        return task

    @marshal_with(taskFields)
    def put(self, pk):
        data = request.json
        task = Task.query.filter_by(id=pk).first()
        task.name = data['name']
        task.location = data['location']
        db.session.commit()
        tasks = tasks = Task.query.all()
        # dataBase[pk]['name'] = data['name']
        # dataBase[pk]['location'] = data['location']
        return tasks

    @marshal_with(taskFields)
    def delete(self, pk):
        task = Task.query.filter_by(id=pk).first()
        db.session.delete(task)
        db.session.commit()
        tasks = tasks = Task.query.all()
        # del dataBase[pk]
        return tasks


api.add_resource(Items, '/')
api.add_resource(Item, '/<int:pk>')


if __name__ == "__main__":
    app.run(debug=True)
