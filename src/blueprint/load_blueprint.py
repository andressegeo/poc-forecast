#coding:utf8
from flask import Blueprint, request
import json
import logging
from datetime import datetime
import bson
from bson import ObjectId
from bson.json_util import dumps
from ..commons.mongodb_model import Document
from .blueprint_utils import flask_construct_response, flask_constructor_error

collection = Document.db.load
""" Loader Blueprint """
LOAD_API_BLUEPRINT = Blueprint(u'load_api', __name__)

@LOAD_API_BLUEPRINT.route(u'/load/', methods=[u'GET'])
def list_loader():
    """
    API LIST Loader
    :return: Flask Response
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date is not None else None
        end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date is not None else None
        if(start_date is not None and end_date is not None):
            try:
                documents = collection.find({
                    "datetime":{"$gt": start_date, "$lt": end_date}
                })
                docs = json.loads(dumps(documents))
                return flask_construct_response({u'items': docs})
            except Exception as err:
                return flask_constructor_error({u'message': err})
        elif(start_date is not None and end_date is None):
            try:
                documents = collection.find({
                    "datetime":{"$gt": start_date}
                })
                docs = json.loads(dumps(documents))
                return flask_construct_response({u'items': docs})
            except Exception as err:
                return flask_constructor_error({u'message': err})
        elif(start_date is None and end_date is not None):
            try:
                documents = collection.find({
                    "datetime":{"$lt": end_date}
                })
                docs = json.loads(dumps(documents))
                return flask_construct_response({u'items': docs})
            except Exception as err:
                return flask_constructor_error({u'message': err})      
        else:
            try:
                documents = collection.find()
                docs = json.loads(dumps(documents))
                return flask_construct_response({u'Documents': docs})
            except Exception as err:
                return flask_constructor_error({u'message': err})
    except Exception as err:
        print err

@LOAD_API_BLUEPRINT.route(u'/load/', methods=[u'POST'])
def add_one_loader():
    """
    API LIST Loader
    :return: Flask Response
    """
    try:
        data = request.get_json(force=True)
    except TypeError as err:
        flask_constructor_error({u'Error': err})
    data["datetime"] = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S UTC')
    document = Document(data)
    try:
        document.save('load')
    except Exception as err:
        return flask_constructor_error({u'message': err}, custom_error_code=400)
    try:
        document = collection.find({
            "_id": ObjectId(document._id)
        })
        doc = json.loads(dumps(document))
        return flask_construct_response({u'item': doc})
    except Exception as err:
        return flask_constructor_error({u'message': err}, custom_error_code=404)

@LOAD_API_BLUEPRINT.route(u'/load/<batch>', methods=[u'POST'])
def add_loader(batch):
    """
    API upload batch Loader
    :return: Flask Response
    """
    batch = "assets/"+ batch + ".json"
    logging.info("filenameee batch is : {}".format(batch))
    try:
        with open(batch, 'r') as f:
            fichier = json.load(f)

    except IOError as err:
        return flask_constructor_error({u'message': err})

    print("typeFichier: {}".format(type(fichier)))
    try:
        for f in fichier:
            f["datetime"] = datetime.strptime(f['datetime'], '%Y-%m-%d %H:%M:%S UTC')
            document = Document(f)
            document.save('load')
        return flask_construct_response({u'items': fichier})
    except Exception as err:
        return flask_constructor_error({u'message': err})

@LOAD_API_BLUEPRINT.route(u'/load/<id>', methods=[u'PUT'])
def update_loader(id):
    """
    API UPDATE Loader
    :return: Flask Response
    """
    if bson.objectid.ObjectId.is_valid(id) != True:
        return flask_constructor_error("{} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string".format(id))

    try:
        data = request.get_json(force=True)
        before = data
    except TypeError as err:
        flask_constructor_error({u'Error': err})
    data["datetime"] = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S UTC')
    document = Document(data)
    document._id = ObjectId(id)
    try:
        document.save('load')
    except Exception as err:
        return flask_constructor_error({u'message': err}, custom_error_code=400)
    try:
        my_document = collection.find({
            "_id": ObjectId(document._id)
        })
        doc = json.loads(dumps(my_document))
        return flask_construct_response({u'item': doc})
    except Exception as err:
        return flask_constructor_error({u'message': err}, custom_error_code=404)

@LOAD_API_BLUEPRINT.route(u'/load/<id>', methods=[u'DELETE'])
def delete_one_loader(id):
    """
    API DELETE Loader
    :return: Flask Response
    """
    if bson.objectid.ObjectId.is_valid(id) !=True:
        return flask_constructor_error("{} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string".format(id))
    
    document = Document()
    document._id = ObjectId(id)
    try:
        document.remove('load')
        return flask_construct_response({u'id ': ObjectId(id)})
    except Exception as err:
        return flask_constructor_error({u'message': err}, custom_error_code=400)


@classmethod
def is_valid(cls, oid):
    try:
        ObjectId(oid)
        return True
    except TypeError:
        return False


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)