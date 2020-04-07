import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

TEST_QUESTIONS = [
    {
        "question": "What's a question?",
        "answer": "I don't know",
        "category": "1",
        "difficulty": "1"
    },
    {
        "question": "What's a question?",
        "answer": "I don't know",
        "category": "1",
        "difficulty": "1"
    },
    {
        "question": "What's a question?",
        "answer": "I don't know",
        "category": "2",
        "difficulty": "1"
    },
    {
        "question": "What's a question?",
        "answer": "I don't know",
        "category": "3",
        "difficulty": "1"
    },
    {
        "question": "What's a question?",
        "answer": "I don't know",
        "category": "3",
        "difficulty": "1"
    },
    {
        "question": "What's a question?",
        "answer": "I don't know",
        "category": "3",
        "difficulty": "1"
    },
    {
        "question": "What's a question?",
        "answer": "I don't know",
        "category": "4",
        "difficulty": "1"
    },
    {
        "question": "What's a question?",
        "answer": "I don't know",
        "category": "4",
        "difficulty": "1"
    },
    {
        "question": "What's a question?",
        "answer": "I don't know",
        "category": "5",
        "difficulty": "1"
    },
    {
        "question": "What's a question?",
        "answer": "I don't know",
        "category": "5",
        "difficulty": "1"
    },
    {
        "question": "What's a question?",
        "answer": "I don't know",
        "category": "5",
        "difficulty": "1"
    },
    {
        "question": "What's a question?",
        "answer": "I don't know",
        "category": "5",
        "difficulty": "1"
    }
]

TEST_CATEGORIES = [
    {
        "type": "category1"
    },
    {
        "type": "category2"
    },
    {
        "type": "category3"
    },
    {
        "type": "category4"
    },
    {
        "type": "category5"
    },
    {
        "type": "category6"
    }
]

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
    ## SHOULD SUCCEED
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['categories'].keys()), 0)

    def test_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['questions']), 0)

    def test_add_question(self):
        questions_before = len(Question.query.all())

        new_question = {
            "question": "Am I a test question?",
            "answer": "Yes, I am",
            "category": 1,
            "difficulty": 2
        }
            
        res = self.client().post('/questions/create', json=new_question)
        data = json.loads(res.data)

        questions_after = len(Question.query.all())

        # cleanup
        to_delete = Question.query.get(data["id"])
        Question.delete(to_delete)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(questions_after - questions_before, 1) # one new question


    def test_search_question(self):
        search_term = {"search_term": "boxer"}

        res = self.client().post('/questions', json=search_term)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(data["count"], 0)

    def test_get_questionsbycategory(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        num_questions = len(Question.query.filter(Question.category == 1).all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["total_questions"], num_questions)

    def test_play_quiz_nocategory_noPreviousQuestions(self):
        quiz_category = {'type': 'click', 'id': 0}
        previous_questions = []

        res = self.client().post('/play', json={
            "quiz_category": quiz_category,
            "previous_questions": previous_questions
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(data["question"]["id"], 0)

    def test_play_quiz_nocategory_withPreviousQuestions(self):
        quiz_category = {'type': 'click', 'id': 0}
        previous_questions = [1, 2, 3, 4, 5]

        res = self.client().post('/play', json={
            "quiz_category": quiz_category,
            "previous_questions": previous_questions
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data["question"]["id"] in previous_questions)

    def test_play_quiz_category1_noPreviousQuestions(self):
        quiz_category = {'type': 'Science', 'id': 1}
        previous_questions = []

        res = self.client().post('/play', json={
            'quiz_category': quiz_category,
            'previous_questions': previous_questions
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["question"]["category"], quiz_category['id'])

    def test_play_quiz_category1_withPreviousQuestions(self):
        quiz_category = {"type": "Science", "id": 1}
        previous_questions = [20, 21]

        res = self.client().post('/play', json={
            'quiz_category': quiz_category,
            'previous_questions': previous_questions
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["question"]["category"], 1)
        self.assertEqual(data["question"]["id"], 22)
        self.assertFalse(data["question"]["id"] in previous_questions)

    # ## SHOULD FAIL

    def test_addquestion_400(self):
        bad_question = {
            "question": "blah blah blah",
            "difficulty": "1"
        }

        res = self.client().post('/questions/create', json=bad_question)
        self.assertEqual(res.status_code, 400)

    def test_play_400(self):
        bad_search = {
            "category": "1",
            "previous_questions": []
        }

        res = self.client().post('/play',json=bad_search)

        self.assertEqual(res.status_code, 400)

    def test_questionsbycategory_404(self):
        res = self.client().get('/categories/100/questions')
        self.assertEqual(res.status_code, 404)

    def delete_question_404(self):
        res = self.client().delete('/questions/1000')
        self.assertEqual(res.status_code, 404)

    def test_generalnotfound_404(self):
        res = self.client().get('/ghiaorhfiod')
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()