from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class ComputerMouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    price = db.Column(db.Integer, unique=False)
    button_count = db.Column(db.Integer, unique=False)
    cable_length = db.Column(db.Integer, unique=False)

    def __init__(self, name, price, button_count, cable_length):
        # super(ComputerMouse, self).__init__(name, price)
        self.button_count = button_count
        self.cable_length = cable_length
        self.name = name
        self.price = price


class GoodSchema(ma.Schema):
    class Meta:
        fields = ('name', 'price', 'button_count', 'cable_length')


good_schema = GoodSchema()
goods_schema = GoodSchema(many=True)
db.create_all()


@app.route("/good", methods=["POST"])
def add_good():
    name = request.json['name']
    price = request.json['price']
    button_count = request.json['button_count']
    cable_length = request.json['cable_length']

    new_good = ComputerMouse(name, price, button_count, cable_length)

    db.session.add(new_good)
    db.session.commit()

    return good_schema.jsonify(new_good)

# endpoint to show all users
@app.route("/good", methods=["GET"])
def get_good():
    all_goods = ComputerMouse.query.all()
    result = goods_schema.dump(all_goods)
    return jsonify(result.data)


# endpoint to get user detail by id
@app.route("/good/<id>", methods=["GET"])
def good_detail(id):
    good = ComputerMouse.query.get(id)
    return good_schema.jsonify(good)


# endpoint to update user
@app.route("/good/<id>", methods=["PUT"])
def good_update(id):
    good = ComputerMouse.query.get(id)
    name = request.json['name']
    price = request.json['price']
    button_count = request.json['button_count']
    cable_length = request.json['cable_length']

    good.name = name
    good.price = price
    good.button_count = button_count
    good.cable_length = cable_length

    db.session.add(good)
    db.session.commit()

    return good_schema.jsonify(good)

# endpoint to delete user
@app.route("/good/<id>", methods=["DELETE"])
def good_delete(id):
    good = ComputerMouse.query.get(id)
    db.session.delete(good)
    db.session.commit()

    return good_schema.jsonify(good)


if __name__ == 'main':
    app.run(debug=True)
