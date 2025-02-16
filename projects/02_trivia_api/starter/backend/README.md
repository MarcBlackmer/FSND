# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

# API ENDPOINT GUIDE

Below, you will find the details of each of the available endpoints in the Trivia application.

## Endpoints list
- GET '/categories'
- GET '/questions'
- GET '/categories/\<id\>/questions'
- DELETE '/questions/\<id\>'
- POST '/questions'
- POST '/quizzes'

Note that all requests will return a status code and success status as True or False.

## Endpoints detail
### GET '/categories'
- **Fetches** a dictionary of categories in which the keys are the IDs and the values are the corresponding strings of the categories
- **Request arguments:** None
- **Returns** an object with a single key (categories) that contains an object of id: category_string key:value pairs as shown here:

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "status_code": 200,
  "success": true
}
```

### GET '/questions'
- **Fetches** a dictionary of categories and a list of paginated questions.
- **Request arguments:** None
- **Returns** category_id: category_type for all available categories and a list of questions with key:value pairs as shown in this example. Additional data returned:
  - Total questions

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "status_code": 200,
  "success": true,
  "total_questions": 19
}
```

### GET '/categories/\<id\>/questions'
- **Fetches** a list of questions based upon the selected category ID
- **Request arguments**: category ID as an integer
- **Returns** a list of questions for that selected category, as well as:
  - Total questions that meet the criterion

Example:

```
{
  "currentCategory": 4,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "status_code": 200,
  "success": true,
  "totalQuestions": 4
}
```
### DELETE '/questions/\<id\>'
- **Deletes** the selected question based upon the question ID
- **Request arguments:** The question ID as an integer
- **Returns** status codes and verification message, as in this example:

```
{
  "message": "Record deleted",
  "status_code": 200,
  "success": true
}
```

### POST '/questions'
This endpoint performs two functions:
- Search for questions based upon a case-insensitive search term
- Create a new question using the new question form

#### Search
- **Request arguments:** Provide a word, multiple words, or partial words in the search field and the input will be used to search the text of questions in the database for any and all matches.
- **Returns** zero to many questions that meet the search criteria. In this example, the search term was "title."

```
{
  "currentCategory": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "status_code": 200,
  "success": true,
  "total_questions": 2
}
```

#### Create a question
- **Request arguments:** The new question submission form provides the fields and options required. The question and answer are submitted by the user. Category and difficulty are provided as options in dropdown menus.
- **Returns** a paginated list of all questions including the recently added question. Additional data:
  - Updated total questions
  - Creation verification message

### POST '/quizzes'
This endpoint randomly selects a question based upon the category selected by the user on the List page. A user may select a given category or "All." The app also keeps track of previously selected questions so as to not provide the same question repeatedly.

- **Receives** a JSON list of previous questions based upon question ID and a JSON dictionary that includes the category and category ID. The category ID for "All" is 0.
- **Fetches** a random question using based upon the category ID and that is not in the list of previous question IDs.
- **Request arguments:** None
- **Returns** a list of previous questions and key:value pairs of question properties. Additional data returned:
  - Quiz category

```
{
  "previousQuestions": [],
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "quiz_category": "1",
  "status_code": 200,
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
