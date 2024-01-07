from flask import Blueprint, render_template, session, redirect, url_for, request
from functools import wraps
from app import db

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
        questions = {
            "question1": [
                {
                    "MCQ1": data['mcq1'],
                    "option1": data['op11'],
                    "option2": data['op12'],
                    "option3": data['op13'],
                    "option4": data['op14']
                },
                {
                    "MCQ2": data['mcq2'],
                    "option1": data['op21'],
                    "option2": data['op22'],
                    "option3": data['op23'],
                    "option4": data['op24']
                },
                {
                    "MCQ3": data['mcq3'],
                    "option1": data['op31'],
                    "option2": data['op32'],
                    "option3": data['op33'],
                    "option4": data['op34']
                }
            ],
            "question2": [
                data['fb1'],
                data['fb2'],
                data['fb3'],
                data['fb4'],
                data['fb5']
            ],
            "question3": [
                data['e1'],
                data['e2'],
                data['e3'],
                data['e4']
            ],
            "question4": [
                data['p1'],
                data['p2']
            ]
        }

        answers = {
            "question1": [
                int(data['q1ans1']),
                int(data['q1ans2']),
                int(data['q1ans3'])
            ],
            "question2": [
                data['q2ans1'],
                data['q2ans2'],
                data['q2ans3'],
                data['q2ans4'],
                data['q2ans5']
            ],
            "question3": [
                data['q3ans1'],
                data['q3ans2'],
                data['q3ans3'],
                data['q3ans4']
            ],
            "question4": [
                data['q4ans1'],
                data['q4ans2']
            ]
        }

        marks = {
            "question1": [
                1,
                1,
                1
            ],
            "question2": [
                1,
                1,
                1,
                1,
                1
            ],
            "question3": [
                5,
                5,
                5,
                5
            ],
            "question4": [
                10,
                10
            ]
        }

        question_paper = {
            "teacherID": teacherID,
            "questionPaperID": data['paper_id'],
            "questionPaperName": data['paper_name'],
            "questions": questions,
            "answers": answers,
            "marks": marks
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
    questions = questionPaper['questions']
    answers = questionPaper['answers']
    return render_template("teacher_view_test.html", paperID=paperID, paperName=paperName, questions=questions, answers=answers)
