from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps
from db import db

student = Blueprint('student', __name__)

# To be put between every route decorator and function if student logged in
def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("student_logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("student_login"))
    return decorated_func


@student.route("/homePage")
@logged_in
def student_home_page():
    return render_template('student_home_page.html')


@student.route("/viewTests")
@logged_in
def student_view_tests():
    studentID = session.get('studentID')
    papers = db.question_papers.find()
    answerPapers = db.answer_papers.find({"studentID": studentID}, {
                                         "questionPaperID": True, "_id": False})
    paperIDList = [paper['questionPaperID'] for paper in answerPapers]
    data = []

    if papers:
        for paper in papers:
            if paper['questionPaperID'] not in paperIDList:
                paperID, paperName = paper['questionPaperID'], paper['questionPaperName']
                data.append((paperID, paperName))
    return render_template('student_view_tests.html', len=len(data), data=data)


@student.route("/viewScores")
@logged_in
def student_view_scores():
    data = []
    studentID = session.get('studentID')
    papers = db.scores.find({"studentID": studentID})

    if papers:
        for answerPaper in papers:

            questionPaperID = answerPaper['questionPaperID']
            score = answerPaper['total']

            questionPaper = db.question_papers.find_one(
                {"questionPaperID": questionPaperID})
            questionPaperName = questionPaper['questionPaperName']

            maximumMarks = questionPaper['maximumMarks']
            
            data.append({'questionPaperID': questionPaperID, 'questionPaperName': questionPaperName, 'score': score, 'maximumMarks': maximumMarks})
    print(data)
    return render_template('student_view_scores.html', data=data, length=len(data))


@student.route("/viewScores/<paperID>")
@logged_in
def student_view_scores_single(paperID):

    # paperID*, paperName*, teacherID*, studentID*, teacherName*, questions*, studentAnswers, referenceAnswer*, individualScore, total, maximumMarks*
    studentID = session.get('studentID')
    questionPaper = db.question_papers.find_one({'questionPaperID': paperID})
    paperName = questionPaper['questionPaperName']
    questions = questionPaper['questions']
    referenceAnswers = questionPaper['answers']
    maximumMarks = questionPaper['maximumMarks']
    teacherID = questionPaper['teacherID']
    teacher = db.teachers.find_one({'teacherID': teacherID})
    teacherName = teacher['teacherName']
    student = db.answer_papers.find_one({'studentID': studentID, 'questionPaperID': paperID})
    studentAnswers = student['answers']
    scores = db.scores.find_one({'studentID': studentID, 'questionPaperID': paperID})
    marksDistribution = scores['score']
    total = scores['total']

    data = {"paperID": paperID, "paperName": paperName, "teacherID": teacherID, "teacherName": teacherName, "questions": questions, "studentAnswers": studentAnswers, "referenceAnswers": referenceAnswers, "marksDistribution": marksDistribution, "total": total, "maximumMarks": maximumMarks}

    return render_template("student_view_scores_single.html", data=data)