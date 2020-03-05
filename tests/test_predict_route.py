import unittest
from mcapi.app import mc_api

class TestApp(unittest.TestCase):

    def start_app(self):
        self.mc_api = mc_api.test_client()





