from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from functools import wraps
from app import mongo

student = Blueprint('student', __name__)

# To be put between every route decorator and function if student logged in
def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("student.student_login"))
    return decorated_func

@student.route("/homePage")
@logged_in
def student_home_page():
    return render_template('student_home_page.html')

@student.route("/viewTests", methods=['GET'])
@logged_in
def student_view_tests():
    if request.method == 'GET':

        papers = mongo.db.question_papers.find()
        if papers:
            data = []
            for paper in papers:
                paperID, paperName = paper['questionPaperID'], paper['questionPaperName']
                data.append((paperID, paperName))
            return render_template('student_view_tests.html', len=len(data), data=data)



