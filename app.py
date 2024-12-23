from flask import Flask, render_template, request, session, redirect, url_for
import time

app = Flask(__name__)
app.secret_key = "mysecretkey"

questions = [
    {"question": "What is 1+1?", "options": ["1", "2", "3", "4"], "answer": "2"},
    {"question": "What is 2+2?", "options": ["1", "2", "3", "4"], "answer": "4"},
    {"question": "What is 3+3?", "options": ["1", "2", "6", "4"], "answer": "6"},
    # Add more questions as needed
]

def initialize_session():
    if 'score' not in session:
        session['score'] = 0
    if 'current_question' not in session:
        session['current_question'] = 0
    if 'start_time' not in session:
        session['start_time'] = time.time()
    if 'reviewed' not in session and 'questions_length' in session:
        session['reviewed'] = [False] * session['questions_length']

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/start_quiz", methods=["GET"])
def start_quiz():
    session.clear()
    session['questions_length'] = len(questions)
    initialize_session()
    return redirect(url_for('quiz'))

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if 'questions_length' not in session:
        return redirect(url_for('home'))

    initialize_session()

    if request.method == "GET" and 'question' in request.args:
        try:
            session['current_question'] = int(request.args.get('question'))
        except (ValueError, IndexError):
            pass

    if session['current_question'] >= session['questions_length']:
        return redirect(url_for('result'))

    if request.method == "POST":
        if 'mark_review' in request.form:
            session['reviewed'][session['current_question']] = True
        selected_answer = request.form.get(f"q{session['current_question']}")
        if selected_answer == questions[session['current_question']]['answer']:
            session['score'] += 1
        session['current_question'] += 1
        return redirect(url_for('quiz'))

    elapsed_time = int(time.time() - session.get('start_time', time.time()))
    time_left = max(0, 600 - elapsed_time)

    if time_left <= 0:
        return redirect(url_for('result'))

    return render_template("index.html", questions=questions, current_question=session['current_question'], time_left=time_left, reviewed=session['reviewed'], questions_length=session['questions_length'])

@app.route("/result")
def result():
    if 'score' not in session:
        return redirect(url_for('home'))
    return render_template("result.html", score=session['score'], total_questions=session['questions_length'])

if __name__ == "__main__":
    app.run(debug=True)