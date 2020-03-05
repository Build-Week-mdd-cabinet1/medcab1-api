import os
import logging


from flask import Blueprint, jsonify, request, render_template
from mcapi.models import db, Strain_data
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from ..api_resources.strain_mod import *


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

primary_routes = Blueprint("primary_routes", __name__)


resPath = os.path.join(os.path.dirname(__file__),
                       '..', 'api_resources')




# class strainSuggester():
    # def __init__(self):
        # self.nn = pickle.load(
            # open(os.path.join(resPath, 'nn.pkl'), 'rb')
        # )

        # self.tfidf = pickle.load(
            # open(os.path.join(resPath, 'tfidf.pkl'), 'rb')
        # )

    # def suggestStrain(self, input_text):
        # tokenize = [token for token in simple_preprocess(input_text)]
        # tokens = self.tfidf.transform(tokenize).todense()
        # return self.nn.kneighbors(tokens)


# model_lr = strainSuggester()


@primary_routes.route("/")
def root():
    return jsonify({"name": "MedCabAPI",
                    "message": "OK"})


@primary_routes.route("/strains/<strain_id>")
def get_strain(strain_id):
    strain = Strain_data.query.filter_by(id=strain_id).first()

    return jsonify({"name": strain.name,
                    "race": strain.race,
                    "description": strain.description})


# TODO: Create route for GET requests from web backend
@primary_routes.route("/predict", methods=["POST"])
def predict():
    user_input = request.get_json()

    _id = user_input["id"]
    race = user_input["race"]
    positive_effects = user_input["positive_effects"]
    negative_effects_avoid = user_input["negative_effects_avoid"]
    ailments = user_input["ailments"]
    flavors = user_input["flavors"]
    additional_desired_effects = user_input["additional_desired_effects"]
    user_id = user_input["user_id"]

    pred_engine = StrainPredictionClass()

    strain_ids = pred_engine.predict(race, positive_effects,
                                     negative_effects_avoid, ailments,
                                     flavors, additional_desired_effects)


    return jsonify({"id": _id,
                    "user_id": user_id,
                    "strain_ids": strain_ids})
                    
@primary_routes.route("/docs")
def read_the_docs():
    return render_template("documentation.html")
