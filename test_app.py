# import os
# import unittest
# import json
# from flask_sqlalchemy import SQLAlchemy

# from app import create_app
# from models import setup_db, Question, Category


# class TriviaTestCase(unittest.TestCase):
#     """This class represents the trivia test case"""

#     def setUp(self):
#         """Define test variables and initialize app."""
#         self.app = create_app()
#         self.client = self.app.test_client
#         self.database_name = "trivia_test"
#         self.database_path = "postgres://{}{}/{}".format('postgres:123456@','localhost:5432', self.database_name)
#         setup_db(self.app, self.database_path)

#         # binds the app to the current context
#         with self.app.app_context():
#             self.db = SQLAlchemy()
#             self.db.init_app(self.app)
#             # create all tables
#             self.db.create_all()
    
#     def tearDown(self):
#         """Executed after reach test"""
#         pass

     
# # /* --------------------------------------------------- Questions - Get --------------------------------------------------- */  
    
#     def test_get_paginated_questions(self):
#         res = self.client().get('/api/questions')
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(data['total_questions'])
#         self.assertTrue(len(data['questions']))
    
    
#     def test_404_sent_requesting_beyond_valid_page(self):
#         res = self.client().get('/questions?page=1000')
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'resource not found')

# # /* ------------------------------------------------- Questions - Search ------------------------------------------------- */  

#     def test_search_questions(self):
#         searchTerm = "actor"
#         res = self.client().post('/api/questions', json={"searchTerm" : searchTerm})
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertEqual(data['searchTerm'], searchTerm)
#         self.assertTrue(data['total_questions'])
#         self.assertTrue(len(data['questions']))


#     def test_search_questions_no_result(self):
#         searchTerm = "TESTING_NO_RESULT"
#         res = self.client().post('/api/questions', json={"searchTerm" : searchTerm})
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertEqual(data['searchTerm'], searchTerm)
#         self.assertEqual(data['total_questions'], 0)
#         self.assertFalse(data['questions'])        

# # /* ------------------------------------------------- Questions - Create ------------------------------------------------- */  

#     def test_create_question(self):
#         question = {
#             "question" : "Test1",
#             "answer" : "Test1",
#             "category" : "1",
#             "difficulty" : "1"
#         }

#         res = self.client().post('/api/questions', json=question)
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)        
#         self.assertTrue(data['created'] > 0)        


#     def test_400_create_question_with_missing_required_parameters(self):
#         question = {
#             #"question" : "Test1",
#             "answer" : "Test1",
#             "category" : "1",
#             "difficulty" : "1"
#         }

#         res = self.client().post('/api/questions', json=question)
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(data['success'], False)        
#         self.assertEqual(data['message'], 'bad request')

# # /* ------------------------------------------------- Questions - Delete ------------------------------------------------- */

#     def test_delete_question(self):
#         question_id = 5
#         res = self.client().delete('/api/questions/{}'.format(question_id))
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)        
#         self.assertEqual(data['deleted'], question_id)                    


#     def test_404_delete_question(self):
#         question_id = 1580
#         res = self.client().delete('/api/questions/{}'.format(question_id))
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)        
#         self.assertEqual(data['message'], 'resource not found')

# # /* --------------------------------------------------- Categories - Get -------------------------------------------------- */ 

#     def test_get_categories(self):
#         res = self.client().get('/api/categories')
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(data['total_categories'])
#         self.assertTrue(len(data['categories']))
    
    
#     def test_get_questions_by_category(self):
#         category_id = "1"
#         category_type = "Science"
#         res = self.client().get('/api/categories/{}/questions'.format(category_id))
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertEqual(data['current_category'], category_type)
#         self.assertTrue(data['total_questions'])   

# # /* ------------------------------------------------------- Quizzes ------------------------------------------------------- */ 

#     def test_quizzes(self):
#         res = self.client().post('/api/quizzes', json={"previous_questions" : [], "quiz_category" : "2"})
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(data['question'])        
    
    
#     def test_quizzes_with_no_more_questions(self):
#         res = self.client().post('/api/quizzes', json={"previous_questions" : [16, 17, 18, 19], "quiz_category" : "2"})
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertFalse(data['question'])  


# # Make the tests conveniently executable
# if __name__ == "__main__":
#     unittest.main()
