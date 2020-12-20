import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class AgencyTestCase(unittest.TestCase):
    """This class represents the Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgres://{}@{}/{}".format(
            'postgres:1234', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.assistant_token = {
            'Authorization': 'Bearer '
            + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkkwZEVCYXRzbHRZVi1mUGNxS3laMSJ9.eyJpc3MiOiJodHRwczovL2ZhcmFoYWxvdGEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZDc5OGYzNzU2Nzk3MDA2OTA3ZjY1ZCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MDg0ODg2MTIsImV4cCI6MTYwODU3NTAxMiwiYXpwIjoidnJ1TWJSazlRTFJjYmp0ZVhldHU1czZYRXV3UEpBa0EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.qcGij6s49dyO8jgbgfa9J8d8xyscGF-pXgu_iyCDjCfyN2d9mdxPKmbkg8MOQkp2AryAuqdv7LeSyLgLJmiO5YPQz68cVPjcnc1aKtUOOemqUY-t4Y1R_dzXmY4qXIUNU14UiXaJS8thnsiBl_ym5edD1rO2IKLrszuXjtD4BQy4jPUPDanTmIY78usYHe0x4NLNNi6hUnybKilCJYkVAn6NWt68IihoH4y-HMToaCesbHIwcaZ8iXTR3Wxzhu0eL-v0-_PbBSFr49jjPRNjozRUpqki21PpLqFz6aWTm97Jvxzc0Vs1qH143ik_wV_VsBVLmMjMQBqYYxp2jKDsWQ'
        }

        self.director_token = {
            'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkkwZEVCYXRzbHRZVi1mUGNxS3laMSJ9.eyJpc3MiOiJodHRwczovL2ZhcmFoYWxvdGEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYWVlNGRmNTJhMjZkMDA2ZTIyY2YyOSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MDg0ODg2NzcsImV4cCI6MTYwODU3NTA3NywiYXpwIjoidnJ1TWJSazlRTFJjYmp0ZVhldHU1czZYRXV3UEpBa0EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.T3xPqE_7I1Qk56MTy8UR_yJk2pIDZ0ttTEKZAx566DkxHeq7SF82BSRepuOGY5VbUP3DEIv00lJ2j80EIYkCL0eLlZ_rhbEBHulwi9uUqOHC19lX6chpBwPOGMM53enBkcfZzN-yqC3umTLtjo44qOeoZxuySVP82F0o71goZ0f5GuuZli2XWSnSxFJxnbvlTGXP4VNCT7Iozy9lTqrZjNCyBlMdtgIBpzlBfTmk2AMizlBDFhurOECdcKAc8VhFXnxXiTXrpzi-cK3uvnNVaY0ftkrpSv0KCk2MzTOwXqwnJ17-hkjgaH1oDeOpfkCtrQRrPquaWlKIVeRs6QazEg'
        }

        self.producer_token = {
            'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkkwZEVCYXRzbHRZVi1mUGNxS3laMSJ9.eyJpc3MiOiJodHRwczovL2ZhcmFoYWxvdGEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZDc5OGI4NzU2Nzk3MDA2OTA3ZjY0MiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MDg0ODg0NzEsImV4cCI6MTYwODU3NDg3MSwiYXpwIjoidnJ1TWJSazlRTFJjYmp0ZVhldHU1czZYRXV3UEpBa0EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.eC4XlqjxAFJJJVNdRycNq3H3KWyDDUzh9095AhCy5ax9CM14WlCl8MSihQNxA-CyqAg0tDUHLYmqMRGp9-8mPs82Dh9JqmXTwDE6gCAbH8nhaSbVygwh0XcSoP8JkNTAxaVX-TrpXpMbG78LDXpXvrGhd8dYUG3ltoLbY5gt7pr8eP3Xihd4Z68GqIRHuD6kHDVCrZqXLTmHrI1XOHO8CimwOGjEUu7bz88_aW5suftUXTq7qRIV1VX-_suWDwrExQP2Odj29vIA0-Sh0unDrXIyTY7QoKzCOQMfkx0476oRIBdY0RjlSHHug57DExjyIQR2Urc-FNy1xpRpqhfHFw'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test for successful operation.
    """

    def test_1_add_actor(self):
        res = self.client().post(
            '/actors',
            json={'name': 'liam neeson', 'age': 68, 'gender': 'male'},
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_2_add_movie(self):
        res = self.client().post(
            '/movies',
            json={'title': 'nona', 'release_date': 2014},
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_3_edit_actor(self):
        res = self.client().patch(
            '/actors/1',
            json={'age': 50},
            headers=self.director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['age'])

    def test_4_edit_movie(self):
        res = self.client().patch(
            '/movies/1',
            json={'title': 'new'},
            headers=self.director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['title'])

    def test_5_get_actors(self):
        res = self.client().get(
            '/actors', headers=self.assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_6_get_movies(self):
        res = self.client().get(
            '/movies', headers=self.assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_7_delete_actors(self):
        res = self.client().delete(
            '/actors/1', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor_id'], 1)

    def test_8_delete_movies(self):
        res = self.client().delete(
            '/movies/1', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie_id'], 1)

    """
    Testing for expected errors
    """

    def test_9_404_delete_unavailable_actor(self):
        res = self.client().delete(
            '/actors/200', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_10_404_delete_unavailable_movie(self):
        res = self.client().delete(
            '/movies/100', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_11_422_add_actor_failed(self):
        res = self.client().post(
            '/actors',
            json={'name': 'mira', 'age': 57, 'gender': ''},
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_12_422_add_movie_failed(self):
        res = self.client().post(
            '/movies',
            json={'title': '', 'release_date': 2020},
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_13_404_edit_actor_failed(self):
        res = self.client().patch(
            '/actors/200',
            json={'age': 30},
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'resource not found')

    def test_14_404_edit_movie_failed(self):
        res = self.client().patch(
            '/movies/100',
            json={'title': 'null'},
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'resource not found')


if __name__ == "__main__":
    unittest.main()
