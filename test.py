from flask import Blueprint, session, redirect, url_for, render_template, request
from functools import wraps
import numpy as np
from app import mongo
from model import evaluateMCQ, evaluateFillBlanks, evaluateBrief

test = Blueprint('test', __name__)

# To be put between every route decorator and function if student logged in
def student_logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("student_logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("student.student_login"))
    return decorated_func

def teacher_logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("teacher_logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("teacher.teacher_login"))
    return decorated_func

@test.route("/attemptTest/<paperID>", methods=['GET', 'POST'])
@student_logged_in
def attempt_test(paperID):
    if request.method == 'POST':

        studentID = session.get('studentID')
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

    studentID = session.get('studentID')
    paper = mongo.db.question_papers.find_one({"questionPaperID": paperID})
    answerPapers = mongo.db.answer_papers.find({"studentID": studentID}, {"questionPaperID": True, "_id": False})
    paperIDList = [paper['questionPaperID'] for paper in answerPapers]
    paperName = paper['questionPaperName']

    if paperID not in paperIDList:
        questions = paper['questions']
        return render_template("attempt_test.html", paperID=paperID, paperName=paperName, questions=questions)
    
    return render_template("test_already_attempted.html", paperName=paperName)

@test.route("/evaluateTest/<paperID>",methods=['GET','POST'])
@teacher_logged_in
def evaluate_test(paperID):

    questionPaper = mongo.db.question_papers.find_one({"questionPaperID": paperID})
    answerPaper = mongo.db.answer_papers.find({"questionPaperID": paperID})
    referenceAnswer = questionPaper['answers']
    marksWeight = questionPaper['marks']

    for paper in answerPaper:
        studentAnswer = paper['answers']

        MCQTotal = evaluateMCQ(studentAnswer['question1'], referenceAnswer['question1'], marksWeight['question1'])
        fillBlanksTotal = evaluateFillBlanks(studentAnswer['question2'], referenceAnswer['question2'], marksWeight['question2'])
        briefTotal = evaluateBrief(studentAnswer['question3'], referenceAnswer['question3'], marksWeight['question3'])
        
        total = int(np.sum(MCQTotal) + np.sum(fillBlanksTotal) + np.sum(briefTotal))

        studentID = paper['studentID']
        score = {
            "question1": MCQTotal,
            "question2": fillBlanksTotal,
            "question3": briefTotal
        }
        scores = {
            "studentID": studentID,
            "questionPaperID": paperID,
            "score": score,
            "total": total
        }
        mongo.db.scores.insert_one(scores)

    return "success"