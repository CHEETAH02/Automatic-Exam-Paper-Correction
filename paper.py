from flask import Blueprint, session, redirect, url_for, render_template, request
from functools import wraps
import numpy as np
from db import db
import PIL
from model import evaluateMCQ, evaluateFillBlanks, evaluateEquations, evaluateBrief
from OCR import requestOCR

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
        questionPaper = db.question_papers.find_one({"questionPaperID": paperID})
        briefAnswers = []

        for row in files:
            try:
                file = files.get(row)
                fileOCR = requestOCR(file)
                briefAnswers.append(fileOCR)

            except PIL.UnidentifiedImageError:
                briefAnswers.append("")

        MCQAnswers = []
        fillBlanksAnswers = []
        equationsAnswers = []

        if 'MCQs' in questionPaper['questions']:
            for i in range(len(questionPaper['questions']['MCQs'])):
                MCQAnswers.append(int(data[f'mcqs_{i + 1}']))

        if 'fillBlanks' in questionPaper['questions']:
            for i in range(len(questionPaper['questions']['fillBlanks'])):
                fillBlanksAnswers.append(data[f'fillblanks_{i + 1}'])

        if 'equations' in questionPaper['questions']:
            for i in range(len(questionPaper['questions']['equations'])):
                equationsAnswers.append(data[f'equations_{i + 1}'])

        studentAnswer = {
            "studentID": studentID,
            "questionPaperID": paperID,
            "answers": {
                "MCQs": MCQAnswers,
                "fillBlanks": fillBlanksAnswers,
                "equations": equationsAnswers,
                "brief": briefAnswers,
            },
        }
        db.answer_papers.insert_one(studentAnswer)
        return render_template("test_submit_success.html")

    studentID = session.get("studentID")
    paper = db.question_papers.find_one({"questionPaperID": paperID})
    paperAlreadyAttended = db.answer_papers.find(
        {"studentID": studentID, "paperID": paperID})

    if len(list(paperAlreadyAttended)) == 0:
        return render_template(
            "attempt_test.html",
            paperID=paperID,
            paperName=paper["questionPaperName"],
            timeAllotted=paper["timeAllotted"],
            questions=paper["questions"]
        )

    return render_template("test_already_attempted.html", paperName=paper["questionPaperName"])


@paper.route("/evaluateTest/<paperID>")
@teacher_logged_in
def evaluate_test(paperID):
    questionPaper = db.question_papers.find_one({"questionPaperID": paperID})
    answerPaper = db.answer_papers.find({"questionPaperID": paperID})
    referenceAnswer = questionPaper["answers"]
    paperName = questionPaper["questionPaperName"]
    marksWeight = questionPaper["marks"]
    studentList = []

    MCQTotal = 0
    fillBlanksTotal = 0
    equationsTotal = 0
    briefTotal = 0

    for paper in answerPaper:
        studentID = paper["studentID"]
        studentEmail = db.students.find_one({"studentID": studentID}, {
                                            "studentEmail": True, "_id": False})
        studentList.append(studentEmail['studentEmail'])
        studentAnswer = paper["answers"]

        if "MCQs" in referenceAnswer:
            MCQTotal = evaluateMCQ(
                studentAnswer["MCQs"],
                referenceAnswer["MCQs"],
                marksWeight["MCQs"],
            )

        if "fillBlanks" in referenceAnswer:
            fillBlanksTotal = evaluateFillBlanks(
                studentAnswer["fillBlanks"],
                referenceAnswer["fillBlanks"],
                marksWeight["fillBlanks"],
            )

        if "equations" in referenceAnswer:
            equationsTotal = evaluateEquations(
                studentAnswer["equations"],
                referenceAnswer["equations"],
                marksWeight["equations"],
                questionPaper["questions"]["equations"]
            )

        if "brief" in referenceAnswer:
            briefTotal = evaluateBrief(
                studentAnswer["brief"],
                referenceAnswer["brief"],
                marksWeight["brief"],
            )

        total = int(np.sum(MCQTotal) + np.sum(fillBlanksTotal) +
                    np.sum(briefTotal) + np.sum(equationsTotal))

        score = {
            "MCQs": MCQTotal,
            "fillBlanks": fillBlanksTotal,
            "equations": equationsTotal,
            "brief": briefTotal,
        }
        scores = {
            "studentID": studentID,
            "questionPaperID": paperID,
            "questionPaperName": paperName,
            "score": score,
            "total": total,
        }

        db.scores.insert_one(scores)
    studentList = ','.join(studentList)
    return redirect(url_for("create_mail", paperID=paperID, paperName=paperName, studentList=studentList))
