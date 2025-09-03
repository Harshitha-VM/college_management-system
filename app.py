from flask import Flask, render_template, request, redirect, session, url_for
from modules.admin import authenticate_admin
from modules.student import authenticate_student, get_student_by_username
from modules.course import get_all_courses, add_course

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if role == 'admin':
            user = authenticate_admin(username, password)
        else:
            user = authenticate_student(username, password)

        if user:
            session['username'] = username
            session['role'] = role
            return redirect(url_for(f'{role}_dashboard'))
        else:
          return "Invalid credentials"

    return render_template('login.html')


@app.route('/admin-dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect('/login')

    courses = get_all_courses()
    return render_template('admin-dashboard.html', courses=courses)


@app.route('/student-dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect('/login')

    student = get_student_by_username(session['username'])
    courses = get_all_courses()
    return render_template('student-dashboard.html', student=student, courses=courses)


@app.route('/add-course', methods=['GET', 'POST'])
def add_course_route():
    if session.get('role') != 'admin':
        return redirect('/login')

    if request.method == 'POST':
        course_name = request.form['course_name']
        add_course(course_name)
        return redirect('/admin-dashboard')

    return render_template('add-course.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
