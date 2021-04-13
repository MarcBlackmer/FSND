import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging

from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    def get_categories_list():
        categories = Category.query.order_by(Category.type).all()
        # the front end is expecting this format to be returned
        category_list = {
            category.id: category.type for category in categories}

        return category_list

    def paginate_questions(request, questions, items_per_page=QUESTIONS_PER_PAGE):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * items_per_page
        end = start + items_per_page

        results = [question.format() for question in questions]

        return results[start:end]

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    def get_categories():

        all_categories = get_categories_list()

        if len(all_categories):
            return jsonify({
                'success': True,
                'status_code': 200,
                'categories': all_categories
            })
        else:
            abort(422)

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions', methods=['GET'])
    def get_questions():

        questions = Question.query.order_by(Question.id).all()
        all_questions = paginate_questions(request, questions)

        all_categories = get_categories_list()

        if len(all_questions):
            return jsonify({
                'success': True,
                'status_code': 200,
                'questions': all_questions,
                'total_questions': (len(questions)),
                'categories': all_categories,
                'current_category': None
            })
        else:
            abort(422)
    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if question is not None:
            question.delete()
            return jsonify({
                'success': True,
                'status_code': 200,
                'message': 'Record deleted'
            })
        else:
            abort(422)

        db.session.close()

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def search_create_question():
        data = request.get_json()

        if 'searchTerm' not in data:
            if (len(data['question']) > 0) & (len(data['answer']) > 0) & (data['difficulty'] is not None) \
                    & (data['category'] is not None):

                new_question = data['question'].strip()
                new_answer = data['answer'].strip()
                new_difficulty = data['difficulty']
                new_category = data['category']

                try:
                    question = Question(question=new_question, answer=new_answer,
                                        difficulty=new_difficulty, category=new_category)
                    question.insert()

                    questions = Question.query.order_by(Question.id).all()
                    all_questions = paginate_questions(request, questions)

                    return jsonify({
                        'success': True,
                        'status_code': 200,
                        'message': 'Question created',
                        'questions': all_questions,
                        'total_questions': (len(questions))
                    })
                except:
                    abort(422)
        else:
            search_term = data['searchTerm'].strip()
            search_data = Question.query.filter(
                Question.question.ilike('%' + search_term + '%')).all()
            questions = [question.format() for question in search_data]
            total_questions = Question.query.count()

            return jsonify({
                'success': True,
                'status_code': 200,
                'questions': questions,
                'total_questions': total_questions,
                'currentCategory': None
            })

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.get_json()

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(400)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'status_code': 400,
            'message': 'Request failed: Please check your syntax and punctuation'
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'status_code': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_error(error):
        return jsonify({
            'success': False,
            'status_code': 422,
            'message': 'Unable to process'
        })

    return app
