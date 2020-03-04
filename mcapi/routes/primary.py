import os
import logging
import pickle


from flask import Blueprint, jsonify, request
from mcapi.models import db, Strain_data
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

primary_routes = Blueprint("primary_routes", __name__)


resPath = os.path.join(os.path.dirname(__file__),
                       '..', 'api_resources')


class strainSuggester():
    def __init__(self):
        self.nn = pickle.load(
            open(os.path.join(resPath, 'nn.pkl'), 'rb')
        )

        self.tfidf = pickle.load(
            open(os.path.join(resPath,'tfidf.pkl'), 'rb')
        )

    def suggestStrain(self, input_text, output_size):
        tokens = self.tfidf.transform([input_text]).todense()
        return self.nn.kneighbors(tokens, n_neighbors=output_size)[1][0]


model_lr = strainSuggester()

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
@primary_routes.route("/predict", methods=["GET","POST"])
def predict():
    user_input = request.get_json()
    prediction = model_lr.suggestStrain(user_input["input"], output_size=1)
    logging.info(prediction)
    pred = int(prediction)
    logging.info(pred)

    res = Strain_data.query.filter(Strain_data.id == pred).all()

    if res == []:
        return jsonify({"message": "list index out of range, try again"})
    else:
        result = res[0]

        return jsonify({'id': result.id,
                    'name': result.name,
                    'race': result.race,
                    'flavors': result.flavors,
                    'positive': result.positive,
                    'negative': result.negative,
                    'medical': result.medical,
                    'rating': result.rating,
                    'description': result.description})



