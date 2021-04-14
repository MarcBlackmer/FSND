import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

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
        category_list = {
            category.id: category.type for category in categories}

        return category_list

    def paginate_questions(request, questions, items_per_page=QUESTIONS_PER_PAGE):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * items_per_page
        end = start + items_per_page

        results = [question.format() for question in questions]

        return results[start:end]

    def get_question_list():
        questions = Question.query.order_by(Question.id).all()

        return questions

    def get_question_by_id(question_id):
        question = Question.query.get(question_id)

        return question

    def get_questions_by_category_id(category_id):
        question = Question.query.filter(Question.category == category_id)

        return question

    def count_questions():
        question_count = Question.query.count()

        return question_count

    def search_questions(search_term):
        search_results = Question.query.filter(
            Question.question.ilike('%' + search_term + '%')).all()

        return search_results

    def get_quiz_question(cat_id, previous_q):
        if cat_id == 0:
            quiz_questions = Question.query.filter(
                Question.id.notin_(previous_q)).all()
        else:
            quiz_questions = Question.query.filter(
                Question.category == cat_id, Question.id.notin_(previous_q)).all()

        quiz_question = random.choice(quiz_questions).format()

        return quiz_question

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

        questions = get_question_list()
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
        question = get_question_by_id(question_id)

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

                    questions = get_question_list()
                    all_questions = paginate_questions(request, questions)

                    return jsonify({
                        'success': True,
                        'status_code': 200,
                        'message': 'Question created',
                        'questions': all_questions,
                        'total_questions': count_questions()
                    })
                except:
                    abort(422)
            else:
                abort(400)
        else:
            try:
                search_term = data['searchTerm'].strip()
                search_data = search_questions(search_term)
                questions_list = paginate_questions(request, search_data)

                i = 0
                for question in search_data:
                    i += 1

                return jsonify({
                    'success': True,
                    'status_code': 200,
                    'questions': questions_list,
                    'total_questions': i,
                    'currentCategory': None
                })
            except:
                abort(422)

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        questions = get_questions_by_category_id(category_id)

        questions_list = [question.format() for question in questions]

        i = 0
        for question in questions_list:
            i += 1

        return jsonify({
            'success': True,
            'status_code': 200,
            'questions': questions_list,
            'totalQuestions': i,
            'currentCategory': category_id
        })

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
    @app.route('/quizzes', methods=['POST'])
    def create_quiz():
        try:
            data = request.get_json()

            if data:

                previous_questions = data['previous_questions']
                category_type = data['quiz_category']['type']
                category_id = data['quiz_category']['id']

                quiz_question = get_quiz_question(
                    category_id, previous_questions)

                return jsonify({
                    'success': True,
                    'status_code': 200,
                    'previousQuestions': previous_questions,
                    'question': quiz_question,
                    'quiz_category': category_id
                })
            else:
                abort(422)
        except:
            abort(422)

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

    @app.errorhandler(405)
    def unprocessable_error(error):
        return jsonify({
            'success': False,
            'status_code': 405,
            'message': 'Sorry. Can\'t do that here'
        })

    @app.errorhandler(422)
    def unprocessable_error(error):
        return jsonify({
            'success': False,
            'status_code': 422,
            'message': 'Unable to process'
        })

    return app
