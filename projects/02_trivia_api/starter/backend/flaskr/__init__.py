import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__)
    setup_db(app)
  
    '''
    TODO: Set up CORS. Allow '*' for origins. 
    Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    

    '''
    TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    
    '''
    # TODO Create an endpoint to handle GET requests for questions
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    #get questions
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        questions_paginated = paginate(request, selection)
        if len(questions_paginated) == 0:
            abort(404)

        categories = Category.query.all()
        categories_all = [category.format() for category in categories]
        
        categories_returned = []
        for cat in categories_all:
            categories_returned.append(cat['type'])
        
        return jsonify({
        'success': True,
        'questions': questions_paginated,
        'total_questions': len(selection),
        'categories': categories_returned,
        'current_category': categories_returned # ???
        })

    
    #delete questions
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):

        question = Question.query.filter(Question.id == question_id).one_or_none()
        if not question:
            abort(400, {'message': 'Question with id {} does not exist.'.format(question_id)})
        

        try:
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except:
            abort(422)
    '''
    # TODO:  Create an endpoint to POST a new question,  
    which will require the question and answer text,  
    category, and difficulty score.
    
    ADDITIONALLY:
    # TODO: Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    '''
    #post questions
    @app.route('/questions', methods=['POST'])
    def create_questions():
        body = request.get_json()

        if not body:
            abort(400, {'message': 'request does not contain a valid JSON body.'})

        search_term = body.get('searchTerm', None)

        if search_term:
            questions = Question.query.filter(Question.question.contains(search_term)).all()

        if not questions:
            abort(404, {'message': 'no questions that contains "{}" found.'.format(search_term)})
        
        questions_found = [question.format() for question in questions]
        selections = Question.query.order_by(Question.id).all() # needed for total_questions
        
        categories = Category.query.all()
        categories_all = [category.format() for category in categories]

        return jsonify({
            'success': True,
            'questions': questions_found,
            'total_questions': len(selections),
            'current_category' : categories_all
        })
        
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        if not new_question:
            abort(400, {'message': 'Question can not be blank'})

        if not new_answer:
            abort(400, {'message': 'Answer can not be blank'})

        if not new_category:
            abort(400, {'message': 'Category can not be blank'})

        if not new_difficulty:
            abort(400, {'message': 'Difficulty can not be blank'})

        try:
            question = Question(
                question = new_question, 
                answer = new_answer, 
                category= new_category,
                difficulty = new_difficulty
                )
            question.insert()

            selections = Question.query.order_by(Question.id).all()
            questions_paginated = paginate(request, selections)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': questions_paginated,
                'total_questions': len(selections)
            })

        except:
            abort(422)

    '''
    TODO: Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    '''
    #post quizzes
    @app.route("/quizzes", methods=['POST'])
    def play_quiz():
        if request.data:
            search_data = json.loads(request.data.decode('utf-8'))
            if (('quiz_category' in search_data
                    and 'id' in search_data['quiz_category'])
                    and 'previous_questions' in search_data):
                questions_query = Question.query.filter_by(
                    category=search_data['quiz_category']['id']
                ).filter(
                    Question.id.notin_(search_data["previous_questions"])
                ).all()
                length_of_available_question = len(questions_query)
                if length_of_available_question > 0:
                    result = {
                        "success": True,
                        "question": Question.format(
                            questions_query[random.randrange(
                                0,
                                length_of_available_question
                            )]
                        )
                    }
                else:
                    result = {
                        "success": True,
                        "question": None
                    }
                return jsonify(result)
            abort(404)
        abort(422,{'message': 'Not valid quizzes posted.'})

    
    #get categories
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()

        if not categories:
            abort(404)

        categories_all = [category.format() for category in categories]
        
        categories_returned = []
        for cat in categories_all:
            categories_returned.append(cat['type'])

        return jsonify({
        'success': True,
        'categories' : categories_returned
        })

    '''
    # TODO: Create a GET endpoint to get questions based on category. 
    '''

    #get questions
    @app.route('/categories/<string:category_id>/questions', methods=['GET'])
    def get_questions_from_categories(category_id):

        questions = (Question.query
        .filter(Question.category == str(category_id))
        .order_by(Question.id)
        .all())

        if not questions:
            abort(400, {'message': 'No questions with category {} found.'.format(category_id) })

        questions_paginated = paginate(request, questions)

        if not questions_paginated:
            abort(404, {'message': 'No questions in selected page.'})

        return jsonify({
        'success': True,
        'questions': questions_paginated,
        'total_questions': len(questions),
        'current_category' : category_id
        })

    #delete categories
    @app.route('/categories/<int:category_id>', methods=['DELETE'])
    def delete_categories(category_id):

        category = Category.query.filter(Category.id == category_id).one_or_none()
        #if no such category
        if not category:
            abort(400, {'message': 'Category with id {} does not exist.'.format(category_id)})
        try:
            category.delete()

            return jsonify({
                'success': True,
                'deleted': category_id
            })

        except:
            abort(422)
    
    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": getError(error, "bad request")
            }), 400

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": getError(error, "resource not found")
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": getError(error, "unprocessable")
            }), 422
    
    #helper methods
    def paginate(request, selection):
        page = request.args.get('page', 1, type=int)
        
        start =  (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    def getError(error, default_text):
        try:
            return error.description["message"]
        except TypeError:
            return default_text

    return app
