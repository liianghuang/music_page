import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #Get question
    def test_404_questions(self):
        request = self.client().get('/question')
        if request.data:
            body = json.loads(request.data)
            self.assertEqual(request.status_code, 404)
            self.assertEqual(body['error'], 404)
            self.assertEqual(body['success'], False)
            self.assertEqual(body['message'], 'resource not found')
  
    #Get category
    def test_invalid_quesiton_in_category(self):
        request = self.client().get('/categories/1000000/questions')
        if request.data:
            body = json.loads(request.data)
            self.assertEqual(request.status_code, 400)
            self.assertEqual(body['error'], 400)
            self.assertEqual(body['success'], False)
            self.assertEqual(body['message'], 'No questions with category 1000000 found.')
    
    #Delete question
    def test_delete_question(self):
        request = self.client().delete('/questions/1000000')
        if request.data:
            body = json.loads(request.data)
            self.assertEqual(request.status_code, 400)
            self.assertEqual(body['error'], 400)
            self.assertEqual(body['success'], False)
            self.assertEqual(body['message'], 'Question with id 1000000 does not exist.')

    #Delete category
    def test_delete_category(self):
        request = self.client().delete('/categories/1000000')
        if request.data:
            body = json.loads(request.data)
            self.assertEqual(request.status_code, 400)
            self.assertEqual(body['error'], 400)
            self.assertEqual(body['success'], False)
            self.assertEqual(body['message'], 'Category with id 1000000 does not exist.')
    
    #Post question
    def test_post_question(self):
        request = self.client().post('/questions')
        if request.data:
            body = json.loads(request.data)
            self.assertEqual(request.status_code, 400)
            self.assertEqual(body['error'], 400)
            self.assertEqual(body['success'], False)
            self.assertEqual(body['message'], 'request does not contain a valid JSON body.')
    
    #Get questions from category
    def test_questions_from_category(self):
        request = self.client().post('/questions')
        if request.data:
            body = json.loads(request.data)
            self.assertEqual(request.status_code, 400)
            self.assertEqual(body['error'], 400)
            self.assertEqual(body['success'], False)
            self.assertEqual(body['message'], 'request does not contain a valid JSON body.')
    
    #Post category
    def test_post_category(self):
        request = self.client().post('/categories')
        if request.data:
            body = json.loads(request.data)
            self.assertEqual(request.status_code, 400)
            self.assertEqual(body['error'], 400)
            self.assertEqual(body['success'], False)
            self.assertEqual(body['message'], 'request does not contain a valid JSON body.')
    
    #Post quizzes
    def test_post_quizzes(self):
        request = self.client().post('/quizzes')
        if request.data:
            body = json.loads(request.data)
            self.assertEqual(request.status_code, 422)
            self.assertEqual(body['error'], 422)
            self.assertEqual(body['success'], False)
            self.assertEqual(body['message'], 'Not valid quizzes posted.')
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()