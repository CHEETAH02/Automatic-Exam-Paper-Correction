from flask import Blueprint, session, redirect, url_for, render_template, request
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

@test.route("/attemptTest/<paperID>", methods=['GET', 'POST'])
@logged_in
def attempt_test(paperID):
    if request.method == 'POST':

        studentID = session['studentID']
        data = request.form
        MCQAnswers = [int(data['group1']), int(data['group2']), int(data['group3'])]
        fillBlanksAnswers = [data['fitb1'], data['fitb2'], data['fitb3'], data['fitb4'], data['fitb5']]
        briefAnswers = [data['brief1'], data['brief2']]

        studentAnswer = {
            "studentID": studentID,
            "questionPaperID": paperID,
            "answers": {
                "question1": MCQAnswers,
                "question2": fillBlanksAnswers,
                "question3": briefAnswers
            }
        }
        mongo.db.answer_papers.insert_one(studentAnswer)
        return render_template('test_submit_success.html')

    studentID = session['studentID']
    paper = mongo.db.question_papers.find_one({"questionPaperID": paperID})
    answerPapers = mongo.db.answer_papers.find({"studentID": studentID}, {"questionPaperID": True, "_id": False})
    paperIDList = [paper['questionPaperID'] for paper in answerPapers]
    paperID = paper['questionPaperID']
    paperName = paper['questionPaperName']

    if paperID not in paperIDList:
        questions = paper['questions']
        return render_template("attempt_test.html", paperID=paperID, paperName=paperName, questions=questions)
    
    return render_template("test_already_attempted.html", paperName=paperName)
    