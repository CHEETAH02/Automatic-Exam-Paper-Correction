from flask import Blueprint, session, redirect, url_for, render_template, request
from functools import wraps
import numpy as np
from app import db
from model import evaluateMCQ, evaluateFillBlanks, expression_trial, evaluateBrief
from OCR import requestOCR, image_to_bytes

test = Blueprint("test", __name__)


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


@test.route("/attemptTest/<paperID>", methods=["GET", "POST"])
@student_logged_in
def attempt_test(paperID):
    if request.method == "POST":
        studentID = session.get("studentID")
        data = request.form
        files = request.files
        briefAnswers = []
        for row in files:
            file = files.get(row)
            briefAnswers.append(image_to_bytes(file))

        MCQAnswers = [int(data["group1"]), int(data["group2"]), int(data["group3"])]
        fillBlanksAnswers = [
            data["fitb1"],
            data["fitb2"],
            data["fitb3"],
            data["fitb4"],
            data["fitb5"],
        ]
        eqanswers = [data["em1"], data["em2"], data["em3"], data["em4"]]

        studentAnswer = {
            "studentID": studentID,
            "questionPaperID": paperID,
            "answers": {
                "question1": MCQAnswers,
                "question2": fillBlanksAnswers,
                "question3": eqanswers,
                "question4": briefAnswers,
            },
        }
        # lines = eqanswers[0].split("\n")
        # print(lines[0])
        # print(lines[1])
        # print(len(lines))
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


@test.route("/evaluateTest/<paperID>")
@teacher_logged_in
def evaluate_test(paperID):
    questionPaper = db.question_papers.find_one({"questionPaperID": paperID})
    answerPaper = db.answer_papers.find({"questionPaperID": paperID})
    referenceAnswer = questionPaper["answers"]
    paperName = questionPaper["questionPaperName"]
    marksWeight = questionPaper["marks"]
    eqquestions=questionPaper["questions"]["question3"]

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
        equationsTotal = expression_trial(
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

        # print("##########################")
        # print(equationsTotal)
        # print("###########################")
        total = int(np.sum(MCQTotal) + np.sum(fillBlanksTotal) + np.sum(briefTotal) + np.sum(equationsTotal))
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
