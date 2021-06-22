
import os
import unittest
import json
import http.client

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Movie, Actor, assigning, setup_db
DOMAINE = os.environ['AUTH0_DOMAIN']
AUDIENCE = os.environ['API_AUDIENCE']
CASTING_ASSISTANT_CID = os.environ['CASTING_ASSISTANT_CID']
CASTING_ASSISTANT_CSEC = os.environ['CASTING_ASSISTANT_CSEC']

CASTING_DIRECTOR_CID = os.environ['CASTING_DIRECTOR_CID']
CASTING_DIRECTOR_CSEC = os.environ['CASTING_DIRECTOR_CSEC']

EXECUTIVE_PRODUCER_CID = os.environ['EXECUTIVE_PRODUCER_CID']
EXECUTIVE_PRODUCER_CSEC = os.environ['EXECUTIVE_PRODUCER_CSEC']
global get_role_token_header


def get_role_token_header(client_id, client_secret, audience=AUDIENCE, domaine=DOMAINE):
    conn = http.client.HTTPSConnection(domaine)
    payload = "{\"client_id\":\""+client_id+"\",\"client_secret\":\""+client_secret + \
        "\",\"audience\":\""+audience+"\",\"grant_type\":\"client_credentials\"}"
    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    d = res.read()
    data = json.loads(d)
    headers = {}
    headers['authorization'] = "Bearer "+data['access_token']
    return headers


casting_assistant = get_role_token_header(
    CASTING_ASSISTANT_CID, CASTING_ASSISTANT_CSEC)
casting_director = get_role_token_header(
    CASTING_DIRECTOR_CID, CASTING_DIRECTOR_CSEC)
executive_producer = get_role_token_header(
    EXECUTIVE_PRODUCER_CID, EXECUTIVE_PRODUCER_CSEC)


class Capstone(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://postgres:0000@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def testa_add_actor(self, role=casting_director):
        print("1")
        res = self.client().post('/actors', headers=role,
                                 json={'name': 'Jin',
                                       'age': 46, 'gender': 'male'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(len('totalActors'))

    def testb_400_add_actor(self, role=executive_producer):

        res = self.client().post('/actors', headers=role,
                                 json={'name': 'Jin',
                                       'age': 46, 'gender': 'maddle'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        self.assertEqual(res.status_code, 400)

    def testc_403_add_actor(self, role=casting_assistant):

        res = self.client().post('/actors', headers=role,
                                 json={'name': 'Jin',
                                       'age': 46, 'gender': 'male'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')

    def testd_edit_actor(self, role=casting_director):
        res = self.client().patch('/actors/1/edit', headers=role,
                                  json={'name': 'Jin',
                                        'age': 26, 'gender': 'female'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(len('actor'))

    def teste_403_edit_actor(self, role=casting_assistant):
        res = self.client().patch('/actors/1/edit', headers=role,
                                  json={'name': 'Jiddn',
                                        'age': 26, 'gender': 'female'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')

    def testf_add_movie(self, role=executive_producer):
        print("2")
        res = self.client().post('/movies', headers=role,
                                 json={'title': 'Fog',
                                       'release_date': '15-03-2020'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(len('totalMovies'))

    def testg_edit_movie(self, role=casting_director):
        print("2")
        res = self.client().patch('/movies/1/edit', headers=role,
                                  json={'title': 'Frog',
                                        'release_date': '15-03-2030'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(len('movie'))

    def testh_404_edit_movie(self, role=casting_director):
        print("2")
        res = self.client().patch('/movies/666/edit', headers=role,
                                  json={'title': 'Frog',
                                        'release_date': '15-03-2030'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def testi_400_add_movie(self, role=executive_producer):

        res = self.client().post('/movies', headers=role,
                                 json={
                                     'release_date': '15-03-2020'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        self.assertEqual(res.status_code, 400)

    def testj_assign_actor_to_movie(self, role=executive_producer):
        print("3")

        res = self.client().post('/assigning', headers=role,
                                 json={'method': 'assign',
                                       'actor_id': 1,
                                       'movie_id': 1})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], 1)
        self.assertEqual(data['movie'], 1)

    def testk_422_assign_actor_to_movie(self, role=casting_director):
        res = self.client().post('/assigning', headers=role,
                                 json={'method': 'assign',
                                       'actor_id': 1000,
                                       'movie_id': 1000})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def testl_403_unassign_actor_to_movie(self, role=casting_assistant):
        res = self.client().post('/assigning', headers=role,
                                 json={'method': 'unassign',
                                       'actor_id': 1,
                                       'movie_id': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')

    def testm_get_actors(self, role=casting_director):
        res = self.client().get('/actors', headers=role)
        data = json.loads(res.data)
        # self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        self.assertTrue(data['totalActors'])

    def testn_get_movies(self, role=casting_assistant):
        res = self.client().get('/movies', headers=role)
        data = json.loads(res.data)
        # self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
        self.assertTrue(data['totalMovies'])

    def testo_get_actor_movies(self, role=executive_producer):
        res = self.client().get('/actors/1/movies', headers=role)
        data = json.loads(res.data)
        # self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def testp_get_movie_actors(self, role=casting_assistant):
        res = self.client().get('/movies/1/actors', headers=role)
        data = json.loads(res.data)
        # self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def testq_404_get_actor_movies(self, role=casting_director):
        res = self.client().get('/actors/1000/movies', headers=role)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def testr_404_get_movie_actors(self, role=casting_director):
        res = self.client().get('/movies/1000/actors', headers=role)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def tests_unassign_actor_to_movie(self, role=casting_director):
        print("4")

        res = self.client().post('/assigning', headers=role,
                                 json={'method': 'unassign',
                                       'actor_id': 1,
                                       'movie_id': 1})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], 1)
        self.assertEqual(data['movie'], 1)

    def testt_404_delete_actor(self, role=casting_director):
        res = self.client().delete('/actors/1000', headers=role)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def testu_403_delete_actor(self, role=casting_assistant):
        res = self.client().delete('/actors/1', headers=role)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')

    def testv_delete_actor(self, role=casting_director):
        print("5")

        res = self.client().delete('/actors/1', headers=role)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(data['totalActors'], 0)

    def testw_403_delete_movie(self, role=casting_director):
        res = self.client().delete('/movies/1', headers=role)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')

    def testx_delete_movie(self, role=executive_producer):
        print("6")

        res = self.client().delete('/movies/1', headers=role)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(data['totalMovies'], 0)

# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
