from bson import ObjectId
from flask import Blueprint, jsonify, request
from mongo_client import Mongo2Client
from flask import request, jsonify
from bson import ObjectId

equipement_tournoi_bp = Blueprint('equipement', __name__)

db_equipement = Mongo2Client().db['equipement_tournoi']


@equipement_tournoi_bp.route('/', methods=['GET'])
def get_all_equipements_tournoi():
    equipements_tournoi = db_equipement.find()
    equipemement_list = []
    for equipement in equipements_tournoi:
        equipement['_id'] = str(equipement['_id'])
        equipemement_list.append(equipement)
    return jsonify(equipemement_list)


@equipement_tournoi_bp.route('/<string:id_equipement_tournoi>', methods=['GET'])
def get_equipement_by_id(id_equipement_tournoi):
    equipement_tournoi = db_equipement.find_one({'_id': ObjectId(id_equipement_tournoi)})
    if equipement_tournoi:
        equipement_tournoi['_id'] = str(equipement_tournoi['_id'])
        return jsonify(equipement_tournoi)
    else:
        return jsonify({'erreur': f"les équipements d'identifiant {id_equipement_tournoi} n'existe pas."}), 404


@equipement_tournoi_bp.route('/', methods=['POST'])
def add_equipement():
    data = request.get_json()

    insert_equipement = db_equipement.insert_one(data)
    if insert_equipement:
        return jsonify({"True": "La requete a bien été insérée"})
    else:
        return jsonify({"False": "Erreur lors de l'insertion"}), 404


@equipement_tournoi_bp.route('/<string:id_equipement_tournoi>', methods=['DELETE'])
def delete_equipement_by_id(id_equipement_tournoi):
    delete_equipement_tournoi = db_equipement.delete_one({'_id': ObjectId(id_equipement_tournoi)})
    if delete_equipement_tournoi:
        return jsonify({"True": "La suppression a bien été réalisée."})
    else:
        return jsonify({'False': 'Erreur lors de la suppression'}), 404


@equipement_tournoi_bp.route('/<string:id_equipement_tournoi>', methods=['PUT'])
def update_equipement_by_id(id_equipement_tournoi):
    data = request.json

    update_equipement_tournoi = db_equipement.update_one({'_id': ObjectId(id_equipement_tournoi)}, {'$set': data})

    if update_equipement_tournoi.modified_count > 0:
        return jsonify({"True": "La mise à jour a bien été réalisée."})
    else:
        return jsonify({'False': 'Erreur lors de la mise à jour'}), 404
