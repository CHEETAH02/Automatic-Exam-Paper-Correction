from flask import Blueprint, render_template, session, redirect, url_for, request
from functools import wraps
from db import db

teacher = Blueprint('teacher', __name__)

# To be put between every route decorator and function if teacher logged in


def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("teacher_logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("teacher_login"))
    return decorated_func


@teacher.route("/homePage")
@logged_in
def teacher_home_page():
    return render_template('teacher_home_page.html')


@teacher.route("/addTest", methods=['GET', 'POST'])
@logged_in
def add_test():
    if request.method == 'POST':
        teacherID = session.get('teacherID')
        data = request.form

        questions = {}
        answers = {}
        marks = {}
        total = 0

        if int(data['mcq_count']) > 0:
            MCQlist = [{
                "question": data[f"mcq{i}"],
                "options": [data[f"op{i}{j}"] for j in range(1, 5)]
            } for i in range(1, int(data['mcq_count']) + 1)]
            questions["MCQs"] = MCQlist

            MCQAnswerlist = [int(data[f"mcq_ans{i}"]) for i in range(1, int(data['mcq_count']) + 1)]
            answers["MCQs"] = MCQAnswerlist

            marks["MCQs"] = int(data["mcq_marks"])
            
            total += (int(data['mcq_count']) * int(data["mcq_marks"]))

        if int(data['fitb_count']) > 0:
            fillBlanksList = [data[f"fitb{i}"] for i in range(1, int(data['fitb_count']) + 1)]
            questions["fillBlanks"] = fillBlanksList

            fillBlanksAnswerList = [data[f"fitb_ans{i}"] for i in range(1, int(data['fitb_count']) + 1)]
            answers["fillBlanks"] = fillBlanksAnswerList

            marks["fillBlanks"] = int(data["fitb_marks"])

            total += (int(data['fitb_count']) * int(data["fitb_marks"]))

        if int(data['equation_count']) > 0:
            equationList = [data[f"equation{i}"] for i in range(1, int(data['equation_count']) + 1)]
            questions["equations"] = equationList

            equationAnswerList = [data[f"equation_ans{i}"] for i in range(1, int(data['equation_count']) + 1)]
            answers["equations"] = equationAnswerList

            marks["equations"] = int(data["eq_marks"])

            total += (int(data['equation_count']) * int(data["eq_marks"]))

        if int(data['brief_count']) > 0:
            briefList = [data[f"brief{i}"] for i in range(1, int(data['brief_count']) + 1)]
            questions["brief"] = briefList

            briefAnswerList = [data[f"brief_ans{i}"] for i in range(1, int(data['brief_count']) + 1)]
            answers["brief"] = briefAnswerList

            marks["brief"] = int(data["brief_marks"])

            total += (int(data['brief_count']) * int(data["brief_marks"]))

        question_paper = {
            "teacherID": teacherID,
            "questionPaperID": data['paper_id'],
            "questionPaperName": data['paper_name'],
            "timeAllotted": data['time_allotted'],
            "questions": questions,
            "answers": answers,
            "marks": marks,
            "maximumMarks": total
        }

        db.question_papers.insert_one(question_paper)
        return render_template('test_added.html')

    return render_template('teacher_add_test.html')


@teacher.route("/viewPapers")
@logged_in
def view_question_papers():
    teacherID = session.get("teacherID")
    question_papers = db.question_papers.find({"teacherID": teacherID})
    corrected_papers = db.scores.find(
        {}, {"questionPaperID": True, "_id": False})
    corrected_papers = [paper['questionPaperID'] for paper in corrected_papers]
    c_data = []
    nc_data = []

    for paper in question_papers:
        if paper['questionPaperID'] not in corrected_papers:
            attended = db.answer_papers.count_documents(
                {"questionPaperID": paper['questionPaperID']})
            paperID = paper['questionPaperID']
            paperName = paper['questionPaperName']
            nc_data.append((paperID, paperName, attended))
        else:
            attended = db.answer_papers.count_documents(
                {"questionPaperID": paper['questionPaperID']})
            paperID = paper['questionPaperID']
            paperName = paper['questionPaperName']
            c_data.append((paperID, paperName, attended))

    return render_template('teacher_view_papers.html', nc_len=len(nc_data), nc_data=nc_data, c_len=len(c_data), c_data=c_data)


@teacher.route("/viewPapers/<paperID>")
@logged_in
def teacher_view_test(paperID):
    questionPaper = db.question_papers.find_one({"questionPaperID": paperID})
    paperName = questionPaper['questionPaperName']
    timeAllotted = questionPaper['timeAllotted']
    questions = questionPaper['questions']
    answers = questionPaper['answers']
    return render_template("teacher_view_test.html", paperID=paperID, paperName=paperName, timeAllotted=timeAllotted, questions=questions, answers=answers)
