import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app, Movie, Actor

ASSISTANT_TOKEN = os.environ['ASSISTANT_TOKEN']
DIRECTOR_TOKEN = os.environ['DIRECTOR_TOKEN']
PRODUCER_TOKEN = os.environ['PRODUCER_TOKEN']


def get_valid_movie_id():
    movie = Movie.query.first()
    return movie.format()['id']


def get_valid_actor_id():
    actor = Actor.query.first()
    return actor.format()['id']


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client

    def tearDown(self):
        """Executed after reach test"""

        pass

# /* -------------- Movies - Get -------------- */

    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization':
                                         'Bearer {}'.format(PRODUCER_TOKEN)
                                         })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_401_get_movies_without_token(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

# /* -------------- Movies - Post -------------- */

    def test_post_movies(self):
        res = self.client().post('/movies',
                                 headers={'Authorization':
                                          'Bearer {}'.format(PRODUCER_TOKEN)
                                          },
                                 json={'title': 'The Story of Unit Testing',
                                       'release_date': '2020-01-01'
                                       })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])

    def test_400_post_movies_with_missing_title(self):
        res = self.client().post('/movies',
                                 headers={'Authorization':
                                          'Bearer {}'.format(PRODUCER_TOKEN)
                                          },
                                 json={'release_date': '2020-01-01'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

# /* -------------- Movies - Patch -------------- */

    def test_patch_movies(self):
        movie_id = get_valid_movie_id()
        res = self.client().patch('/movies/{}'.format(movie_id),
                                  headers={'Authorization':
                                           'Bearer {}'.format(PRODUCER_TOKEN)
                                           },
                                  json={'title':
                                        'The Story of Unit Testing II',
                                        'release_date': '2021-01-01'
                                        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])

    def test_404_patch_movies_with_wrong_id(self):
        res = self.client().patch('/movies/99999',
                                  headers={'Authorization':
                                           'Bearer {}'.format(PRODUCER_TOKEN)
                                           },
                                  json={'title':
                                        'The Story of Unit Testing II',
                                        'release_date': '2021-01-01'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

# /* -------------- Movies - Delete -------------- */

    def test_delete_movies(self):
        movie_id = get_valid_movie_id()
        res = self.client().delete('/movies/{}'.format(movie_id),
                                   headers={'Authorization':
                                            'Bearer {}'.format(PRODUCER_TOKEN)
                                            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['delete'], movie_id)

    def test_404_delete_movies_with_wrong_id(self):
        res = self.client().delete('/movies/999999',
                                   headers={'Authorization':
                                            'Bearer {}'.format(PRODUCER_TOKEN)
                                            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

# /* -------------- Actors - Get -------------- */

    def test_get_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                         'Bearer {}'.format(PRODUCER_TOKEN)
                                         })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_401_get_actors_without_token(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

# /* -------------- Actors - Post -------------- */

    def test_post_actors(self):
        res = self.client().post('/actors',
                                 headers={'Authorization':
                                          'Bearer {}'.format(PRODUCER_TOKEN)
                                          },
                                 json={'name': 'Denzel Washington',
                                       'date_of_birth': '1954-12-28',
                                       'gender': 'male'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_400_post_actors_with_missing_name(self):
        res = self.client().post('/actors',
                                 headers={'Authorization':
                                          'Bearer {}'.format(PRODUCER_TOKEN)
                                          },
                                 json={'date_of_birth': '1954-12-28'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

# /* -------------- Actors - Patch -------------- */

    def test_patch_actors(self):
        actor_id = get_valid_actor_id()
        res = self.client().patch('/actors/{}'.format(actor_id),
                                  headers={'Authorization':
                                           'Bearer {}'.format(PRODUCER_TOKEN)},
                                  json={'name': 'Denzel Washington II',
                                        'date_of_birth': '1954-12-28',
                                        'gender': 'male'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_404_patch_actors_with_wrong_id(self):
        res = self.client().patch('/actors/99999',
                                  headers={'Authorization':
                                           'Bearer {}'.format(PRODUCER_TOKEN)},
                                  json={'name': 'Denzel Washington II',
                                        'date_of_birth': '1954-12-28',
                                        'gender': 'male'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

# /* -------------- Actors - Delete -------------- */

    def test_delete_actors(self):
        actor_id = get_valid_actor_id()
        res = self.client().delete('/actors/{}'.format(actor_id),
                                   headers={'Authorization':
                                            'Bearer {}'.format(PRODUCER_TOKEN)
                                            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['delete'], actor_id)

    def test_404_delete_actors_with_wrong_id(self):
        res = self.client().delete('/actors/999999',
                                   headers={'Authorization':
                                            'Bearer {}'.format(PRODUCER_TOKEN)
                                            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

# /* -------------- RBAC Testing - Casting Assistant -------------- */

    def test_get_movies_by_assistant(self):
        res = self.client().get('/movies',
                                headers={'Authorization':
                                         'Bearer {}'.format(ASSISTANT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_403_patch_movies_by_assistant(self):
        movie_id = get_valid_movie_id()
        res = self.client().patch('/movies/{}'.format(movie_id),
                                  headers={'Authorization':
                                           'Bearer {}'.format(ASSISTANT_TOKEN)
                                           },
                                  json={'title':
                                        'The Story of Unit Testing II',
                                        'release_date': '2021-01-01'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

# /* -------------- RBAC Testing - Casting Director -------------- */

    def test_post_movies_by_director(self):
        res = self.client().post('/actors',
                                 headers={'Authorization':
                                          'Bearer {}'.format(DIRECTOR_TOKEN)},
                                 json={'name': 'Denzel Washington',
                                       'date_of_birth': '1954-12-28',
                                       'gender': 'male'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_403_post_movies_by_director(self):
        res = self.client().post('/movies',
                                 headers={'Authorization':
                                          'Bearer {}'.format(DIRECTOR_TOKEN)},
                                 json={'title': 'The Story of Unit Testing',
                                       'release_date': '2020-01-01'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)


# /* -------------- RBAC Testing - Executive Producer -------------- */
# Executive Producer has been tested in all above tests.

# Make the tests conveniently executable

if __name__ == '__main__':
    unittest.main()
