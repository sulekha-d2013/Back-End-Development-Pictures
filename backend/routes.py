from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for i in data:
        if i["id"] == id:
            return jsonify(i), 200

    return {}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_pic = request.json
    if not new_pic:
        return {"message": "Invalid input parameter"}, 422

    F =None;
    for i in data:
        if i["id"] == new_pic["id"]:
            F = 1;
            break;

    if F == 1:
        return  {'Message':f"picture with id {new_pic['id']} already present"}, 302

    try:
        data.append(new_pic)
    except NameError:
        return {"message": "data not defined"}, 500
    
    return dict(new_pic), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    F=None;
    new_pic = request.json
    for j, i in enumerate(data):
        if i["id"] == id:
            F = j;
            break;

    if F is not None:
        data[F] = new_pic;
        return jsonify(data[F]), 200

    return {}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    F = None;
    for i in data:
         if i["id"] == id:
            F = i;
            break;

    if F is not None:
        data.remove(F)
        return {}, 204

    return {"message": "person not found"}, 404
