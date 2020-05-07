import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, helper_table

# TEST_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
# CASTING_ASSISTANT = os.getenv('CASTING_ASSISTANT')
# CASTING_DIRECTOR = os.getenv('CASTING_DIRECTOR')
# EXECUTIVE_PRODUCER = os.getenv('EXECUTIVE_PRODUCER')

# TEST_DATABASE_URI = 'postgres://postgres@localhost:5432/capstone_db'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlXRTdkaU5pRnVUS1oxWDNzQ1pRWiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2Fwc3RvbmUtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDFkYzkxY2MxYWMwYzE0OGZlNTczIiwiYXVkIjoiY2Fwc3RvbmUtYXBwIiwiaWF0IjoxNTg4ODg1NTgzLCJleHAiOjE1ODg4OTI3ODMsImF6cCI6ImdYS3hhNGwzTGMyczM1WTNldFlMM1JZMXBKUGdKcWZYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.hk0jJSr2nw4b9hBMd3v3iHZrrkO5JjFDfD34WPpFjMg7Ia8bRLE97ffhXswz0YeyULvgSgaP7cjDviQ8FzBTt_i92W-JXug8pXuyZpv4ov1b6w3WiU4-iWyphNtShveCS8uxL_-t5kGMCkXmDOXV6l_y1pzhc4dKkosltXoD4vhroEoR4Ug7cfRtovhvqDwl6Vlrjp4ZKyFS89vvpyvb3XI3VOLCATmPgh1nm2F2VR6VNI1HWvRtyjLOXlF8IG5rwSOaGl0TDI5z7MLuyq603MrnIU9vyJPF0XOvCouvC7Fo4rx16zghux810l5rM3S0D6DW2UVMFOpfTllZXJB8Aw'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlXRTdkaU5pRnVUS1oxWDNzQ1pRWiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2Fwc3RvbmUtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDFmNDAxY2MxYWMwYzE0OGZlYWQwIiwiYXVkIjoiY2Fwc3RvbmUtYXBwIiwiaWF0IjoxNTg4ODg1ODA1LCJleHAiOjE1ODg4OTMwMDUsImF6cCI6ImdYS3hhNGwzTGMyczM1WTNldFlMM1JZMXBKUGdKcWZYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.mQjBOhZfa3AR2CQ63qCJ8IT_qsU58gJSjbSBq6XqKHvn4K4UgxPBNSMSpaLem22tdpCMb5uORoY_r1Ia6h02jZHUXA51gDxbRcflt_03f8MbshzIcOKDe1a8LQbhxpXfNiFi35ZZiRvXBW8SaVGmKyK83oLYIcWn_cRMd9fCGDflOaNXDmSYOASjFbE3VHCW2Q4V0fuevpWN8zje8znKuFKaSRdN_X7YqemVYf45rta88Kv8poS3yLkkr8G4WjI1PWV36wkceIbr1YbauN3D37WYDXf3gKs_AppuikVwCLXI_0nwHnknxwLHQ0zxhgtJUovd1lL-rD3wBNmASTynlg'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlXRTdkaU5pRnVUS1oxWDNzQ1pRWiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2Fwc3RvbmUtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDFmODk2YjY5YmMwYzEyZmY2YmVlIiwiYXVkIjoiY2Fwc3RvbmUtYXBwIiwiaWF0IjoxNTg4ODg1OTA4LCJleHAiOjE1ODg4OTMxMDgsImF6cCI6ImdYS3hhNGwzTGMyczM1WTNldFlMM1JZMXBKUGdKcWZYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.LspDvo6QMXIelXqr8sDxhL7PEkD93s-CRDTHRfT2xN_wOyeLibBzHJGaaYPVrYFHT0hhuN0_lYW-EdRM5BPr4umBwRJwnoYeVjCWfZQo40924dgw3KqlpPSOPqcw9b1Es0lqKQrOTtXvvQyhazaGodIUqR5X_5DhvTPdyen5kC1edGceDQq0kn6oELEWoZPESotslFEs8x9DK_HqNTnfJln5EXSGFUImqtJjcbcnHxI5w8imryloDhb7MAs2_IzfeWDotk763mq3nnVNbtoBzsAig1GbdmhWO4ZbYKTna6IAK7Wb-JJTx8o2P8vzzraeQN4HmfbVMnydcorRbrd-gw'


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'capstone_test'
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, path_db=self.database_path)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create movies
            movie1 = Movie(title='The end',
                           release_date='2020-05-07',
                           )
            self.db.session.add(movie1)
            self.db.session.commit()
            movie2 = Movie(title='Game of thrones',
                           release_date='2020-05-04',
                           )
            self.db.session.add(movie2)
            self.db.session.commit()
            movie3 = Movie(title='The last of us',
                           release_date='2020-05-20',
                           )
            self.db.session.add(movie3)
            self.db.session.commit()

            # create actors
            actor1 = Actor(name='dijon',
                           age=23,
                           gender='Male')
            self.db.session.add(actor1)
            self.db.session.commit()
            actor2 = Actor(name='Nathan',
                           age=18,
                           gender='Male')
            self.db.session.add(actor2)
            self.db.session.commit()
            actor3 = Actor(name='Sarah',
                           age=23,
                           gender='Female')
            self.db.session.add(actor3)
            self.db.session.commit()

    '''
    RBAC TEST
    '''

    def test_post_actors_by_executive_producer_200(self):
        response = self.client().post('/actors', headers={
            "Authorization": "Bearer {}"
                                      .format(EXECUTIVE_PRODUCER)
        },
                                      json={
                                          "name": "Alex",
                                          "gender": "male",
                                          "age": 25,
                                          "movies": [1]
                                      })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_post_actors_by_casting_assistant_401(self):
        response = self.client().post('/actors',
                                      headers={
                                          "Authorization": "Bearer {}"
                                      .format(CASTING_ASSISTANT)
                                      },
                                      json={
                                          "name": "Brandon",
                                          "gender": "male",
                                          "age": 16
                                      })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_post_movies_by_executive_200(self):
        response = self.client().post('/movies',
                                      headers={
                                          "Authorization": "Bearer {}"
                                      .format(EXECUTIVE_PRODUCER)
                                      },
                                      json={
                                          "title": "Prestige",
                                          "release_date": "2020-05-01",
                                          'actors': [2, 1]
                                      })

        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_post_movies_by_casting_assistant_without_auth_401(self):
        response = self.client().post('/movies',
                                      headers={
                                          "Authorization": "Bearer {}"
                                      .format(CASTING_ASSISTANT)
                                      },
                                      json={
                                          "title": "American Made",
                                          "release_date": "05/12/2018",
                                      })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_get_actors_by_casting_assistant_with_auth_200(self):
        response = self.client().get('/actors',
                                     headers={
                                         "Authorization": "Bearer {}"
                                     .format(CASTING_ASSISTANT)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_get_actors_by_casting_assistant_without_auth_401(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'no_auth_header')

    def test_get_movies_by_casting_assistant_with_auth_200(self):
        response = self.client().get('/movies',
                                     headers={
                                         "Authorization": "Bearer {}"
                                     .format(CASTING_ASSISTANT)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_get_movies_by_casting_assistant_without_auth_401(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'no_auth_header')

    def test_patch_actors_by_casting_director_with_auth_200(self):  #
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
                                           "Authorization": "Bearer {}".format(CASTING_DIRECTOR)
                                       },
                                       json={
                                           "name": "David",
                                           "gender": "other",
                                           "age": 10,
                                           "movies": [1]
                                       })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_patch_actors_by_casting_assistant_without_auth_401(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
                                           "Authorization": "Bearer {}".format(CASTING_ASSISTANT)
                                       },
                                       json={
                                           "name": "David",
                                           "gender": "other",
                                           "age": 10,
                                           "movies": [1]
                                       })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_patch_movies_by_casting_director_with_auth_200(self):  #
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().patch('/movies/{}'.format(random_id),
                                       headers={
                                           "Authorization": "Bearer {}".format(CASTING_DIRECTOR)
                                       },
                                       json={
                                           "title": "Joker",
                                           "release_date": "2019-10-1",
                                           "cast": [1]
                                       })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_patch_movies_by_casting_assistant_without_auth_401(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().patch('/movies/{}'.format(random_id),
                                       headers={
                                           "Authorization": "Bearer {}".format(CASTING_ASSISTANT)
                                       },
                                       json={
                                           "title": "Joker",
                                           "release_date": "2019-10-1",
                                       })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_delete_actors_by_casting_assistant_without_auth_401(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().delete('actors/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                        .format(CASTING_ASSISTANT)
                                        }
                                        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_delete_actors_by_executive_producer_with_auth_200(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().delete('actors/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                        .format(EXECUTIVE_PRODUCER)
                                        }
                                        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_delete_movies_by_casting_assistant_without_auth_401(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().delete('movies/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                        .format(CASTING_ASSISTANT)
                                        }
                                        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_delete_movies_by_executive_producer_with_auth_200(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().delete('movies/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                        .format(EXECUTIVE_PRODUCER)
                                        }
                                        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()
