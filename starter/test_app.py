import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlXRTdkaU5pRnVUS1oxWDNzQ1pRWiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2Fwc3RvbmUtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDFkYzkxY2MxYWMwYzE0OGZlNTczIiwiYXVkIjoiY2Fwc3RvbmUtYXBwIiwiaWF0IjoxNTg5MDI2NzExLCJleHAiOjE1ODkwMzUxMTEsImF6cCI6ImdYS3hhNGwzTGMyczM1WTNldFlMM1JZMXBKUGdKcWZYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.BGdFZuyKQDJdqNBdnzZ-6BxTjG7T5TLurMXm7nEA-WxwfLu3QQl7lQXPOsDeAd3IdisgZORcTsLnga4CAql6YD50FYB2SZ0TzxyKY_sLIOX8nceHDcqdoSi-9iEJWojaa4HyoAgCBCKNsOLAGi93JqVYio5E9LP5lmNF1L287UrkL6HCcE8mrwamlbjsevIzJQppZn6duPmgAv71pKLtt3Nm8glvxLP1qS8YkYx95Go9MRsxWrOua3jH3rN976xXo6caoyAFd5IxNaxMan3HFoyojEyrE4Jprid5lWmbgHUeSyEHMSiRZGEE8zWXOysk1-hdd7rnJfNQf3f3kEdLVw'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlXRTdkaU5pRnVUS1oxWDNzQ1pRWiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2Fwc3RvbmUtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDFmNDAxY2MxYWMwYzE0OGZlYWQwIiwiYXVkIjoiY2Fwc3RvbmUtYXBwIiwiaWF0IjoxNTg5MDIxNjU1LCJleHAiOjE1ODkwMjg4NTUsImF6cCI6ImdYS3hhNGwzTGMyczM1WTNldFlMM1JZMXBKUGdKcWZYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.PSjuwFnvqGIUfuEYZiDDDyssi6VoA2Q-99jSZqS50RqrZIUH327VDS6VLHZu_UiSAtnU8jYjzndhrDjG0yhSaTOPlzpntCTfv4rnTYY7couWAj3-ZGkjcTZyXcfuuj3GTmDXkeQpCjlw5010spWM_08p8-vpy1_xNo1ERYf0k4gioBQVWNtOovkbtjJ3vtfBlIjuIDeQy0TSzp40vtIhfaDmD00nMJg1v_4Jgrd_dzhBlEoZyn_nOY3_yleypeehEPbjzbsxzuZuaThKLdDhxCBxMZexn4BAgW2w89LdEy55uZoGO36OFPeDekVPUdWDqajHPCJRwrBHHMD0c6FLLg'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlXRTdkaU5pRnVUS1oxWDNzQ1pRWiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2Fwc3RvbmUtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDFmODk2YjY5YmMwYzEyZmY2YmVlIiwiYXVkIjoiY2Fwc3RvbmUtYXBwIiwiaWF0IjoxNTg5MDIxNzI4LCJleHAiOjE1ODkwMjg5MjgsImF6cCI6ImdYS3hhNGwzTGMyczM1WTNldFlMM1JZMXBKUGdKcWZYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.gM-5q0MOzvR0nrn12C9YpAdd6i8rfC0C-kSZ84V05sgkAWzrNNssrvo16ov-JiH-2IiZa9jcsqjF4v4nDiLgfEomA-qU90-FfiRHl3G1i3KS_C2dksjdun96PWkEU5u5U3eupSj6UqmPwevr2xaHhzlmZohBtU0TsarLWnTXB1rR_r70B98sAwFaA-9nEAnhGR3tZorg0eXgnLSRMvDQBGzKr_i4XiBQE_tkAf_K3pWg5xdTcbqaSV5uEjAPwuPGB0mexSmOVIn5Af_2Z0Z7YvYqaZ9OQt77RbOgI8ZF2W85GQmN9qYtALG1aKP0egkjCmEmE5nWDEWm5LCVKScqvg'


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
        response = self.client().post('/assign_movie_to_actor/',
                                      headers={
                                          "Authorization": "Bearer {}"
                                      .format(EXECUTIVE_PRODUCER)
                                      },
                                      json={
                                          "actor_id": 1,
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
