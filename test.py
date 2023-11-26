from flask import Blueprint, session, redirect, url_for, render_template
from functools import wraps
from app import mongo

test = Blueprint('test', __name__)

# To be put between every route decorator and function if student logged in
def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("student.student_login"))
    return decorated_func

@test.route("/attemptTest/<paperID>", methods=['GET'])
def attempt_test(paperID):
    paper = mongo.db.question_papers.find_one({"questionPaperID": paperID})
    name = paper['questionPaperName']
    questions = paper['questions']
    return render_template("attempt_test.html", name=name, questions=questions)