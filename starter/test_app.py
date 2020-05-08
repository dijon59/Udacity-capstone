import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

# TEST_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
# CASTING_ASSISTANT = os.getenv('CASTING_ASSISTANT')
# CASTING_DIRECTOR = os.getenv('CASTING_DIRECTOR')
# EXECUTIVE_PRODUCER = os.getenv('EXECUTIVE_PRODUCER')


CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlXRTdkaU5pRnVUS1oxWDNzQ1pRWiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2Fwc3RvbmUtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDFkYzkxY2MxYWMwYzE0OGZlNTczIiwiYXVkIjoiY2Fwc3RvbmUtYXBwIiwiaWF0IjoxNTg4OTI3MDMzLCJleHAiOjE1ODg5MzQyMzMsImF6cCI6ImdYS3hhNGwzTGMyczM1WTNldFlMM1JZMXBKUGdKcWZYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.CBDrG5L0kF5eD-wQDi2hdpwg079ioN5dTeKmdK16iKtwMCIzdI3JibMkvYR8rBxIkjfxb1_qLOOIvxfoP5F3QTV5S6HoXvagiqhB-9LMG-o_mr7wgQKG8hUBGpcNcAof-HSY3YwnAuUXclqi_UWPSq6sYt35eIoxs-EBVVs5oHeWw0h3Acca-eIZHfr6UbN88KkTWFaM2ltxkWfhy0vYSy8jNIosbPQ6MnHL8oZkPyOU1ZJkge17YC4Jn2rzWlI_iPSvnI37fnxgrK4XU1RMUOaiuUsLzmXxy_stJLerGenao88uNOhKN-J89qgRtgNzZkYEgYsMkHf-AnO137eCSg'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlXRTdkaU5pRnVUS1oxWDNzQ1pRWiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2Fwc3RvbmUtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDFmNDAxY2MxYWMwYzE0OGZlYWQwIiwiYXVkIjoiY2Fwc3RvbmUtYXBwIiwiaWF0IjoxNTg4OTI3MTUwLCJleHAiOjE1ODg5MzQzNTAsImF6cCI6ImdYS3hhNGwzTGMyczM1WTNldFlMM1JZMXBKUGdKcWZYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.TTJg_OL_Z4isQarRcMBZ1RlRZRI4c8Ld05LLOkzQIOIx7ZYj4rTgY7tcKHPPk4aJuRMoTuHjQOgVids2kcx2kEsiOqLQQxFcoqoyCNl9azC7JXd1ai_iQmb3ES-D0imY5gd_YNgaMxEaaDpCh6oSSlSLx6rvsOkcPX1eb27rjAPiM7yuEZsa_vXZz2lCWjfCaSLNOzaB2coEpsYUEwwxzO5eMZLUOhDE4PeIhvyHyMeRoiCm6qZmhbaAf-sRQLgZN8SZHVkT6YDE8HtxuzUfg_oAIxXpnb89g_lfrbHHHbt8_cid09etbgw8hkvw4jCipNn8dRUDsXiK1cweyQpL8Q'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlXRTdkaU5pRnVUS1oxWDNzQ1pRWiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2Fwc3RvbmUtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDFmODk2YjY5YmMwYzEyZmY2YmVlIiwiYXVkIjoiY2Fwc3RvbmUtYXBwIiwiaWF0IjoxNTg4OTI3MjIxLCJleHAiOjE1ODg5MzQ0MjEsImF6cCI6ImdYS3hhNGwzTGMyczM1WTNldFlMM1JZMXBKUGdKcWZYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.GJ6Nmyw53NPAmjl1SSilqOg2Y9CpjF59PV64FHIo9dfjSXNN1jvfb9g9DY-RNrt5w9_OZQ4KfzgN0wTtI7_d-hYw168-yI79n8PeTQz-TlwT3vsf8CGhUQzbpxa3TOlAuEWqAfK8T28FNHzRXfOqJ8My-1fcEN-DUUVwCvbuBcL_J-vfr70d9QLnI_hiAkgsCG_XW_ttVvPh__v0kgR47tSzBL5-K4qF94EBkojaBk_H-ahf3k0sfWY_FY8Sp2eZNcpdQ3uBhzf4Y9Vh6y-409iJ7CQPyp5b347CO0bOFMRNfA_jrcAvRsuu8YXwpaA_d_v5BaxDmC1xYUk6OxuMxQ'


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
                                          "name": "Fred",
                                          "gender": "male",
                                          "age": 25,
                                          "movies": [3]
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
                                          "name": "Michel",
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
                                          'actors': [3]
                                      })

        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_post_movies_by_casting_assistant_401(self):
        response = self.client().post('/movies',
                                      headers={
                                          "Authorization": "Bearer {}"
                                      .format(CASTING_ASSISTANT)
                                      },
                                      json={
                                          "title": "The white house down",
                                          "release_date": "05/12/2018",
                                      })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_get_actors_by_casting_assistant_200(self):
        response = self.client().get('/actors',
                                     headers={
                                         "Authorization": "Bearer {}"
                                     .format(CASTING_ASSISTANT)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_get_actors_by_casting_assistant_401(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'no_auth_header')

    def test_get_movies_by_casting_assistant_200(self):
        response = self.client().get('/movies',
                                     headers={
                                         "Authorization": "Bearer {}"
                                     .format(CASTING_ASSISTANT)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_get_movies_by_casting_assistant_401(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'no_auth_header')

    def test_patch_actors_by_casting_director_200(self):  #
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
                                           "Authorization": "Bearer {}".format(CASTING_DIRECTOR)
                                       },
                                       json={
                                           "name": "David",
                                           "gender": "other",
                                           "age": 10,
                                           "movies": [3]
                                       })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_patch_actors_by_casting_assistant_401(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
                                           "Authorization": "Bearer {}".format(CASTING_ASSISTANT)
                                       },
                                       json={
                                           "name": "David",
                                           "gender": "other",
                                           "age": 10,
                                           "movies": [3]
                                       })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_patch_movies_by_casting_director_200(self):  #
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().patch('/movies/{}'.format(random_id),
                                       headers={
                                           "Authorization": "Bearer {}".format(CASTING_DIRECTOR)
                                       },
                                       json={
                                           "title": "Joker",
                                           "release_date": "2019-10-1",
                                           "cast": [4]
                                       })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_patch_movies_by_casting_assistant_401(self):
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

    def test_delete_actors_by_casting_assistant_401(self):
        response = self.client().delete('actors/1',
                                        headers={
                                            "Authorization": "Bearer {}"
                                        .format(CASTING_ASSISTANT)
                                        }
                                        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_delete_actors_by_executive_producer_with_auth_200(self):
        response = self.client().delete('actors/2',
                                        headers={
                                            "Authorization": "Bearer {}"
                                        .format(EXECUTIVE_PRODUCER)
                                        }
                                        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_delete_movies_by_casting_assistant_401(self):
        response = self.client().delete('movies/1',
                                        headers={
                                            "Authorization": "Bearer {}"
                                        .format(CASTING_ASSISTANT)
                                        }
                                        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_delete_movies_by_executive_producer_200(self):
        response = self.client().delete('movies/2',
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
