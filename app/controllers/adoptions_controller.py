from flask import current_app, jsonify, request
from app.models.adoptions_model import AdoptionsModel
from app.exc.exc_pet import NoDataFound
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm.exc import DetachedInstanceError
from app.models.pet_model import PetsModel

# from flask_jwt_extended import jwt_required


# @jwt_required()
def post_pet():
    try:
        session = current_app.db.session

        data = request.get_json()

        select_pet = PetsModel.query.filter_by(id=data["pet_id"]).one()

        data.pop("pet_id")
        data["pet_info"] = select_pet

        pet = AdoptionsModel(**data)

        session.add(pet)
        session.commit()

        return jsonify(data=pet)
    except IntegrityError as e:
        return {"Error": str(e.orig).split("\n")[0]}, 400


# @jwt_required()
def get_all():
    try:
        data = AdoptionsModel.query.all()

        if data == []:
            raise NoDataFound

        return jsonify(data=data)
    except NoDataFound:
        return jsonify({"message": "No data found."}), 400


# @jwt_required()
def delete_data():
    try:
        session = current_app.db.session

        data = request.get_json()
        query = AdoptionsModel.query.filter_by(id=data['id']).one()

        session.delete(query)
        session.commit()

        return "", 204
    except KeyError:
        return {'message': 'Invalid key'}, 404
    except NoResultFound:
        return {
            'message': 'No lines were found when one was needed'
            }, 404
    except DetachedInstanceError as e:
        return {
            'message': str(e)
            }, 404


# @jwt_required()
def patch_data():
    try:
        session = current_app.db.session
        data = request.get_json()

        query = AdoptionsModel.query.filter_by(id=data['id']).one()

        for key, value in data.items():
            setattr(query, key, value)

        session.add(query)
        session.commit()

        return '', 204
    except KeyError:
        return {'message': 'Invalid key'}, 404
    except AttributeError:
        return {'message': 'No data found.'}, 404


def adotar_pet():
    try:
        session = current_app.db.session

        data = request.json

        adopted_pet = AdoptionsModel(**data)

        session.add(adopted_pet)
        session.commit()

        return jsonify(adopted_pet), 201
    except IntegrityError as e:
        erro = str(e.orig).split(' "')[0]
        if erro == 'duplicate key value violates unique constraint':
            return {'Error': 'Este pet ja foi adotado.'}, 400
        elif erro == 'insert or update on table':
            return {'Error': 'Este pet nao existe.'}, 404

            
def select_data():
    try:
        data = request.get_json()

        query = AdoptionsModel.query.filter_by(id=data['id']).one()

        return jsonify(data=query)

    except NoDataFound:
        return jsonify({"message": "No data found."}), 400
