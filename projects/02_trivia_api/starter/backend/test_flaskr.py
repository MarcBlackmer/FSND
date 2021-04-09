import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
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

    def test_listCategories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        # Test that the response code is equal to our expectation
        self.assertEqual(response.status_code, 200)
        # Test success response is equal
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_listCategories_failure(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No categories found')

    def test_listQuestions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'] == None)

    def test_listQuestions_failure(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No questions found')

    def test_deleteQuestion(self):
        dummy_question = Question(
            question='dummy question', answer='dummy answer', difficulty=5, category=1)
        db.session.add(dummy_question)
        db.session.commit()

        question_id = str(dummy_question.id)

        response = self.client().delete('/questions/' + question_id)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Record deleted')

    def test_deleteQuestion_failure(self):
        response = self.client().delete('/questions/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Record not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
