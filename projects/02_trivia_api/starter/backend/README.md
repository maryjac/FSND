# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

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


## Endpoints
GET '/categories'
GET '/questions'
GET '/categories/<category_id>/questions'
POST '/questions'
POST '/questions/create'
POST '/play'
GET '/questions<question_id>

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

### GET '/questions'
- Fetches a list of all questions, paginated in groups of 10
- Request arguments: (optional) page number
- Returns: int "count" total number of questions; and a list "questions" of objects with id: int (unique), question: string, answer: string, difficulty: int, category: int category_id
 ```
 {
   "count": 3,
    "questions": [
        {
        "answer": "Lake Victoria", 
        "category": 3, 
        "difficulty": 2, 
        "id": 1, 
        "question": "What is the largest lake in Africa?"
        }, 
        {
        "answer": "The Palace of Versailles", 
        "category": 3, 
        "difficulty": 3, 
        "id": 2, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
        }, 
        {
        "answer": "Agra", 
        "category": 3, 
        "difficulty": 2, 
        "id": 3, 
        "question": "The Taj Mahal is located in which Indian city?"
        }   
    ]
}
```

### GET '/categories/<category_id>/questions'
- Fetches questions by a given category id
- Request arguments: int category_id
- Returns: string name of given category, int total questions belonging to category, and list of objects "questions" with int id, string question, string answer, int difficulty, string category type
```
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": "Science", 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": "Science", 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": "Science", 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "total_questions": 3
}
```

## POST '/questions'
- Searches for questions
- Required arguments: string "search_term", case insensitive
- Returns a list of "questions" objects which contain a substring of the search term, and int "count" the number of objects returned by the search
```
{
  "count": "3", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": "Science", 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": "Science", 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": "Science", 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
} 
```

## POST '/questions/create'
- Creates a new question
- Required arguments: body with string question, string answer, int difficulty (1-5), and int category id (1-6)
- Returns: int "id" of new question
```
{"id": 25}
```

## POST '/play'
- Fetches a random question not played in the game before and (optional) belongs to a given category
- Required arguments: list "previous_questions" of int question.ids, can be empty
- Optional arguments: int "category_id" (1-6)
- Returns: object "question" and int "id" of that question
```
    {
    "id": 21,
    "question": {
      "answer": "Alexander Fleming", 
      "category": "Science", 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
```

## DELETE '/questions<question_id>'
- Deletes a question from the database
- Required arguments: int question_id of the question you want to delete
- Returns: int "question_id" of successfully deleted question
```
{id: 5}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

