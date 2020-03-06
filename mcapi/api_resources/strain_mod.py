import os
import pickle
import logging


import numpy as np
import pandas as pd
from gensim.utils import simple_preprocess


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logging.disable(logging.INFO)


# Converts the lists of strings into normal strings
def check_nans(x):
    if x is None:
        return ""
    else:
        return x


def convert_string_to_list(x):
    converted = (
        str(x).strip("]['").replace("'", "").replace("\n", "").split(', ')
    )
    return converted


def filter_function(model_recommendations, user_positive,
                    user_negative, user_flavors):

    output_tier_zero_list = []
    output_tier_one_list = []
    output_tier_two_list = []
    output_tier_three_list = []

    for row in model_recommendations:

        strain_id = row[0]
        strain_flavors = row[1]
        strain_positive = row[2]
        strain_negative = row[3]

        logging.info("strain_id: " + str(strain_id))
        logging.info("strain_id type: " + str(type(strain_id)))

        strain_positive_list = convert_string_to_list(
                                   check_nans(strain_positive)
                               )
        strain_negative_list = convert_string_to_list(
                                   check_nans(strain_negative)
                               )
        strain_flavors_list = convert_string_to_list(
                                  check_nans(strain_flavors)
                              )

        user_positive_list = convert_string_to_list(check_nans(user_positive))
        user_negative_list = convert_string_to_list(check_nans(user_negative))
        user_flavors_list = convert_string_to_list(check_nans(user_flavors))

        output_tier_zero_list.append(strain_id)

        positive_check = False
        flavors_check = False
        negative_check = False

        for i in strain_positive_list:
            if i in user_positive_list:
                if positive_check is False:

                    output_tier_one_list.append(strain_id)
                    positive_check = True

                for i in strain_flavors_list:
                    if i in user_flavors_list:
                        if flavors_check is False:

                            output_tier_two_list.append(strain_id)
                            flavors_check = True

                        if (
                          'Anxious' not in user_negative_list or
                          'Paranoid' not in user_negative_list
                        ):
                            if negative_check is False:

                                output_tier_three_list.append(strain_id)
                                negative_check = True

                        else:
                            pass
                else:
                    pass
        else:
            pass

    x = output_tier_three_list
    unique_list_tier_three = x

    if len(unique_list_tier_three) >= 10:
        while len(unique_list_tier_three) > 10:
            unique_list_tier_three.pop()

        return unique_list_tier_three

    else:

        x = output_tier_two_list
        unique_list_tier_two = x

        if len(unique_list_tier_two) >= 10:
            while len(unique_list_tier_two) > 10:
                unique_list_tier_two.pop()

            return unique_list_tier_two

        else:

            x = output_tier_one_list
            unique_list_tier_one = x

            if len(unique_list_tier_one) >= 10:
                while len(unique_list_tier_one) > 10:
                    unique_list_tier_one.pop()

                return unique_list_tier_one

            else:

                x = output_tier_zero_list
                unique_list_tier_zero = x

                if len(unique_list_tier_zero) >= 10:
                    while len(unique_list_tier_zero) > 10:
                        unique_list_tier_zero.pop()

                    return unique_list_tier_zero

                else:

                    return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


resPath = os.path.dirname(__file__)


class StrainPredictionClass():
    def __init__(self):
        with open(os.path.join(resPath, 'nn.pkl'), 'rb') as n_n:
            self.nn = pickle.load(n_n)
        with open(os.path.join(resPath, 'tfidf.pkl'), 'rb') as vectorizer:
            self.tfidf = pickle.load(vectorizer)

    def predict(self, user_race, user_positive, user_negative,
                user_medical, user_flavors, user_additional_desired_effects):

        tokenize = [token for token in simple_preprocess(user_medical)]
        tokens = self.tfidf.transform(tokenize).todense()
        nn_model_recommendations = self.nn.kneighbors(tokens)

        for element in nn_model_recommendations:
            logging.info(element[0])
            for member in element:
                logging.info(type(member))

        list_50 = list(nn_model_recommendations[1][0])
        nn_model_recommendations_list = list_50

        strain_url = (
          'https://raw.githubusercontent.com/Build-Week-mdd-cabinet1/' +
          'Data-Science/Tyler-Russin/strain_data.csv'
        )
        df_strains = pd.read_csv(strain_url)
        df_top_50_recommendations = []

        df_strains = df_strains.fillna("")
        logging.info("df_strains fillna executed")

        for recommendation_id in nn_model_recommendations_list:
            result = df_strains.iloc[recommendation_id]

            result = [
                result['Id'], result['Flavors'],
                result['Positive'], result['Negative']
            ]
            df_top_50_recommendations.append(result)

        filtered_recommendation_list = filter_function(
                                         model_recommendations=(
                                           df_top_50_recommendations
                                         ),
                                         user_positive=user_positive,
                                         user_negative=user_negative,
                                         user_flavors=user_flavors
                                       )

        return filtered_recommendation_list


model_lr = StrainPredictionClass()
