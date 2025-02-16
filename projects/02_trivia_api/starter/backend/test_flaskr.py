import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, db, Question, Category

DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'udacity')
DB_PWD = os.getenv('DB_PWD', '')
DB_NAME = os.getenv('DB_NAME', 'trivia_test')
DB_PATH = 'postgresql://{}/{}'.format(DB_HOST, DB_NAME, DB_USER, DB_PWD)


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_NAME
        self.database_path = DB_PATH
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
        self.assertEqual(data['status_code'], 200)
        # Test success response is equal
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_listCategories_fail_405(self):
        response = self.client().post('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['status_code'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Sorry. Can\'t do that here')

    def test_listQuestions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'] == None)

    def test_listQuestions_fail_500(self):
        response = self.client().post('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['status_code'], 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], 'Internal server error')

    def test_deleteQuestion(self):
        dummy_question = Question(
            question='dummy question', answer='dummy answer', difficulty=5, category=1)
        db.session.add(dummy_question)
        db.session.commit()

        question_id = str(dummy_question.id)

        response = self.client().delete('/questions/' + question_id)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Record deleted')

    def test_deleteQuestion_fail_422(self):
        response = self.client().delete('/questions/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['status_code'], 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to process')

    def test_questionCreate(self):
        question_name = 'new_question'
        dummy_question = {'question': question_name,
                          'answer': 'new_answer',
                          'difficulty': '1',
                          'category': '1'}

        response = self.client().post('/questions', json=dummy_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question created')
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

        # Remove the test question from the database
        try:
            Question.query.filter_by(question=question_name).delete()
            db.session.commit()
        except:
            db.session.rollback()

    def test_questionCreate_fail_400(self):
        dummy_question = {'question': '', 'answer': 'test_answer',
                          'difficulty': '1', 'category': '3'}

        response = self.client().post('/questions', json=dummy_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status_code'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'Request failed: Check your syntax and punctuation')

    def test_searchQuestion(self):
        search_term = {'searchTerm': 'tItLE'}

        response = self.client().post('/questions', json=search_term)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_searchQuestion_blank(self):
        search_term = {'searchTerm': ' '}

        response = self.client().post('/questions', json=search_term)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_questionByCategory(self):

        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_questionByCategory_fail_400(self):
        # Test requesting a category ID that doesn't exist
        response = self.client().get('/categories/1000/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status_code'], 400)

    def test_quiz(self):
        submission = {"previous_questions": [],
                      "quiz_category": {"type": "Science", "id": 1}}

        response = self.client().post('/quizzes', json=submission)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['previousQuestions'], [])
        self.assertTrue(data['question'])
        self.assertEqual(data['quiz_category'], 1)

    def test_quiz_fail(self):
        submission = {'previous_questions': [
            1, 2], 'quiz_category': {'type': 'Science', 'id': 1}}

        response = self.client().get('/quizzes', json=submission)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['status_code'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], 'Sorry. Can\'t do that here')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
