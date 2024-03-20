from flask import Blueprint, session, redirect, url_for, render_template, request
from functools import wraps
import numpy as np
from db import db
import requests
import PIL
import posixpath
from model import evaluateMCQ, evaluateFillBlanks, evaluateEquations, evaluateBrief
from OCR import requestOCR, image_to_bytes

paper = Blueprint("paper", __name__)


# To be put between every route decorator and function if student logged in
def student_logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("student_logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("student_login"))

    return decorated_func

# To be put between every route decorator and function if teacher logged in
def teacher_logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("teacher_logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("teacher_login"))

    return decorated_func

@paper.route("/confirmStart/<paperID>")
@student_logged_in
def confirm_start(paperID):
    paperName = request.args.get('paperName')
    return render_template("test_confirm_start.html", paperID=paperID, paperName=paperName)

@paper.route("/attemptTest/<paperID>", methods=["GET", "POST"])
@student_logged_in
def attempt_test(paperID):
    if request.method == "POST":
        
        studentID = session.get("studentID")
        data = request.form
        files = request.files
        briefAnswers = []

        for row in files:
            try:
                file = files.get(row)
                briefAnswers.append(image_to_bytes(file))
                
            except PIL.UnidentifiedImageError:
                base_url = request.url_root.rstrip('/')
                image_url = url_for('static', filename='not_submitted.jpg')
                external_image_url = posixpath.join(base_url, image_url.lstrip('/'))
                response = requests.get(external_image_url)
                briefAnswers.append(response.content)

        MCQAnswers = [int(data["group1"]), int(
            data["group2"]), int(data["group3"])]
        fillBlanksAnswers = [
            data["fitb1"],
            data["fitb2"],
            data["fitb3"],
            data["fitb4"],
            data["fitb5"],
        ]
        equationAnswers = [data["em1"], data["em2"], data["em3"], data["em4"]]

        studentAnswer = {
            "studentID": studentID,
            "questionPaperID": paperID,
            "answers": {
                "question1": MCQAnswers,
                "question2": fillBlanksAnswers,
                "question3": equationAnswers,
                "question4": briefAnswers,
            },
        }
        db.answer_papers.insert_one(studentAnswer)
        return render_template("test_submit_success.html")

    studentID = session.get("studentID")
    paper = db.question_papers.find_one({"questionPaperID": paperID})
    answerPapers = db.answer_papers.find(
        {"studentID": studentID}, {"questionPaperID": True, "_id": False}
    )
    paperIDList = [paper["questionPaperID"] for paper in answerPapers]
    paperName = paper["questionPaperName"]

    if paperID not in paperIDList:
        questions = paper["questions"]
        return render_template(
            "attempt_test.html",
            paperID=paperID,
            paperName=paperName,
            questions=questions,
        )

    return render_template("test_already_attempted.html", paperName=paperName)


@paper.route("/evaluateTest/<paperID>")
@teacher_logged_in
def evaluate_test(paperID):
    questionPaper = db.question_papers.find_one({"questionPaperID": paperID})
    answerPaper = db.answer_papers.find({"questionPaperID": paperID})
    referenceAnswer = questionPaper["answers"]
    paperName = questionPaper["questionPaperName"]
    marksWeight = questionPaper["marks"]
    eqquestions = questionPaper["questions"]["question3"]

    for paper in answerPaper:
        studentAnswer = paper["answers"]

        for index in range(len(studentAnswer["question4"])):
            studentAnswer["question4"][index] = requestOCR(
                studentAnswer["question4"][index]
            )

        MCQTotal = evaluateMCQ(
            studentAnswer["question1"],
            referenceAnswer["question1"],
            marksWeight["question1"],
        )
        fillBlanksTotal = evaluateFillBlanks(
            studentAnswer["question2"],
            referenceAnswer["question2"],
            marksWeight["question2"],
        )
        equationsTotal = evaluateEquations(
            studentAnswer["question3"],
            referenceAnswer["question3"],
            marksWeight["question3"],
            eqquestions
        )
        briefTotal = evaluateBrief(
            studentAnswer["question4"],
            referenceAnswer["question4"],
            marksWeight["question4"],
        )

        total = int(np.sum(MCQTotal) + np.sum(fillBlanksTotal) +
                    np.sum(briefTotal) + np.sum(equationsTotal))
        studentID = paper["studentID"]
        score = {
            "question1": MCQTotal,
            "question2": fillBlanksTotal,
            "question3": equationsTotal,
            "question4": briefTotal,
        }
        scores = {
            "studentID": studentID,
            "questionPaperID": paperID,
            "questionPaperName": paperName,
            "score": score,
            "total": total,
        }
        db.scores.insert_one(scores)

    return render_template("teacher_test_corrected.html")
