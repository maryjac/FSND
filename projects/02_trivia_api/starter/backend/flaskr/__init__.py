import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sqlalchemy
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  db = SQLAlchemy(app)
  setup_db(app)

  CORS(app, resources={r"/*/": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, DELETE, POST')
    return response

  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    data = {}

    for c in categories:
      data[c.id] = c.type

    return jsonify({'categories': data})

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
    questions = Question.query.all()
    questions_formatted = [{
      'id': q.id,
      'question': q.question,
      'answer': q.answer,
      'difficulty': q.difficulty,
      'category': q.category
     } for q in questions]

    num_questions = len(questions)
    categories = Category.query.all()
    categories_formatted = {}
    
    for c in categories:
      categories_formatted[c.id] = c.type

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10

    if (page > end):
      abort(404)

    data = {
      'success': True,
      'categories': categories_formatted,
      'questions': questions_formatted[start:end],
      'total_questions': num_questions,
      'current_category': 'None'
    }

    return jsonify(data)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      question.delete()
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()
    
    return jsonify({'id': question_id})

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions/create', methods=['POST'])
  def add_question():
    json = request.get_json()
    
    ks = json.keys()
    data = {}

    try:
      data = {
        "question": json['question'],
        "answer": json['answer'],
        "difficulty": json['difficulty'],
        "category": json['category']
      } 
    except:
      abort(400)

    question = Question(**data)
    Question.insert(question)
    return jsonify({ 'id': question.id })

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def search_questions():
    search_term = request.form.get('search_term', '')
  
    if (search_term is None):
      abort(400)

    questions = Question.query.filter(\
      Question.question.ilike('%' + search_term + '%')
      ).all()

    results = {
      "count": len(questions),
      "questions": [{
        "id": q.id,
        "question": q.question,
        "answer": q.answer,
        "difficulty": q.difficulty,
        "category": q.category
      } for q in questions]
    }

    return jsonify(results)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category_id>/questions')
  def get_questions_by_category(category_id):
    if Category.query.get(category_id) is None:
      abort(404)
      
    questions = Question.query.filter(Question.category == category_id)
    current_category = Category.query.get(category_id).type

    questions_formatted = [{
      "id": q.id,
      "question": q.question,
      "answer": q.answer,
      "difficulty": q.difficulty,
      "category": current_category,
    } for q in questions]

    return jsonify({
      "current_category": current_category,
      "total_questions": len(questions_formatted),
      "questions": questions_formatted
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
  @app.route('/play', methods=['POST'])
  def play():
    body = request.get_json()
    possible_questions = []
  
    try:
      quiz_category = int(body['quiz_category']['id'])
      previous_questions = body['previous_questions']
    except:
      abort(400)
    
    if (quiz_category > 0):
      possible_questions = Question.query.filter(\
        Question.category == quiz_category,
        Question.id.notin_(previous_questions)).all()
    else:
      possible_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()

    question = random.choice(possible_questions)

    question_formatted = {
      "id": question.id,
      "question": {
        "question": question.question,
        "answer": question.answer,
        "category": question.category,
        "id": question.id
      }
    }

    return jsonify(question_formatted)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_formatting(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad formatting"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
    }), 404

  @app.errorhandler(422)
  def not_processable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Not processable"
    }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Unexpected server error"
    }), 500

  return app

    