import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlXRTdkaU5pRnVUS1oxWDNzQ1pRWiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2Fwc3RvbmUtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDFkYzkxY2MxYWMwYzE0OGZlNTczIiwiYXVkIjoiY2Fwc3RvbmUtYXBwIiwiaWF0IjoxNTg4OTM4NDQzLCJleHAiOjE1ODg5NDU2NDMsImF6cCI6ImdYS3hhNGwzTGMyczM1WTNldFlMM1JZMXBKUGdKcWZYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.GOSm417wdPaCHiCoFsJH7fnicvwaAjJxEkfIVe8evXk-WTrUVKiI0vdT5X5zfSgZ8YV_fytnkeF3t4uqYV3TwVQebcPW1FEchbJLTheOPuBH4oRGPbmtx9L2fjZsL99kBH7auGLLWd0DayUaseXt0f16pv-KlSe3f4HQmIW79KKhtPO_6WioQS3z-PS0ryhJ7sIv2w-dAB3G3nwXC1azK55s5LXaxS9s5Q4Ap-g3mIuQGnGyieWWpRHvAt9zrS-JtZFqtbpl7uGh9VT5BeARYs_-VoBxTaGSnT12brtkv4R87cWJP5ZH3p9z-WJkJpOgu3rB-8CZ1UFRDHUp7B2pWQ'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlXRTdkaU5pRnVUS1oxWDNzQ1pRWiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2Fwc3RvbmUtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDFmNDAxY2MxYWMwYzE0OGZlYWQwIiwiYXVkIjoiY2Fwc3RvbmUtYXBwIiwiaWF0IjoxNTg4OTM4NTMyLCJleHAiOjE1ODg5NDU3MzIsImF6cCI6ImdYS3hhNGwzTGMyczM1WTNldFlMM1JZMXBKUGdKcWZYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.Ego26tyfdDsqtgW2yGQffB6CsU2qvMrp6gq5kuMCnPRgAM542P08s4NaXgFnHjYb8EjNmpFZ7sIWTAbkTfFEAEx_i7lmvLVgfQeYKsQTxuW74mWDMU399K-jnlUNy9qfYxvgXKwgyX1rXqDfl7R8OaFEgoYn1TgjcElKyfYU1HczvqzypI7tQhonuCyoNgjLhO1Pib5b3IGcO6c7dN0VTfTas20jFdUt5uU_CRC2eXW_QJM1TTJLW87e0bkEZn_mJmrvyIJv0cDEV79KisVqGih18-RZhpq7HvxDiRSyeJZ80c6s4eX6UmiMFGpA2Qyi9nbtiXsG4V9Ea0lYuDxEsw'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlXRTdkaU5pRnVUS1oxWDNzQ1pRWiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2Fwc3RvbmUtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDFmODk2YjY5YmMwYzEyZmY2YmVlIiwiYXVkIjoiY2Fwc3RvbmUtYXBwIiwiaWF0IjoxNTg4OTM4NjA5LCJleHAiOjE1ODg5NDU4MDksImF6cCI6ImdYS3hhNGwzTGMyczM1WTNldFlMM1JZMXBKUGdKcWZYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.dZBXa-6HfVbhayfPQ9Bsiu1si67Ws2RZpCRnO1Eb1sWCS523Fe8R8XzbzwcGnJCVpMGmDtzq7yQCFWuVSE6N6vfaCl5-Sor2wDU8Z0ZO_Q_rCuTqxldCGrrTnqQRo5NoNM6GWl_CcOAmGCeIXUkBHYCSdgsb_gaHCmCrQLTiB7oFiRrK7bZorttOGyRhaEZcZc5ZkscVbAtpyv84gPv-rIX7U3qOefWRgew-HZupGvszvW2eXHWW8Wly62tFROfuaBigwEfDhI4MAy_bSZXwo1UUO0Gn1rf4xAsSDvxoWjvpuPYqxJe5NnLsKXCebpSTDaQqvAQDiCL5x_B6vl9z2Q'


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
        response = self.client().post('/actors',
                                      json={
                                          "name": "Fred",
                                          "gender": "male",
                                          "age": 25,
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
                                           "name": "Tresor",
                                           "gender": "Male",
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
                                           "name": "Tresor",
                                           "gender": "Male",
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
                                           "title": "Anaconda 3",
                                           "release_date": "2020-10-1",
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
                                           "title": "Anaconda 3",
                                           "release_date": "2020-10-1",
                                       })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_post_actors_assigned_movie_by_executive_200(self):
        response = self.client().post('/actors/assign_movie/',
                                      headers={
                                          "Authorization": "Bearer {}"
                                      .format(EXECUTIVE_PRODUCER)
                                      },
                                      json={
                                          "actor_id": 2,
                                          "movie_id": 1,
                                      })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

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
