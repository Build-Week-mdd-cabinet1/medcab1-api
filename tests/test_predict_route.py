import unittest
from mcapi.app import mc_api


class TestApp(unittest.TestCase):

    def setUp(self):
        self.mc_api = mc_api.test_client()

    def tearDown(self):
        pass

    def test_predict_route(self):
        payload = {
            "id": 1,
            "race": "hybrid",
            "positive_effects": "",
            "negative_effects_avoid": "",
            "ailments": "Inflammation, Eye Pressure",
            "flavors": "",
            "additional_desired_effects": "I want to feel a sense of calm",
            "user_id": 10
        }
        response = self.mc_api.post("/predict", json=payload)
        json_response = {'id': 1,
                         'strain_id': [
                            962, 357, 604, 1365, 1332,
                            1293, 1815, 365, 343, 214
                         ],
                         'user_id': 10}
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, json_response)

    def test_predict_no_id(self):
        payload = {
            "race": "hybrid",
            "positive_effects": "",
            "negative_effects_avoid": "",
            "ailments": "Inflammation, Eye Pressure",
            "flavors": "",
            "additional_desired_effects": "I want to feel a sense of calm",
            "user_id": 10
        }
        response = self.mc_api.post("/predict", json=payload)

        print(response.json)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
