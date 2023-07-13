"""Flask app for Cupcakes"""


import time

from flask import Flask, jsonify, make_response, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import Cupcake, connect_db, db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    return render_template('index.html', time=time.time())

@app.route("/api/cupcakes")
def show_all_cupcakes():
    """For every cupcake in the cupcakes database, serialize and turn into JSON"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=all_cupcakes)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Serialize a single cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes", methods=["POST"])
def new_cupcake():
    """Create a new cupcake"""

    new_cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"],
        image=request.json["image"],
    )
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a Cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete Cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
