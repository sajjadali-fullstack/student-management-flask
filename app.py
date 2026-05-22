from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'Hello World!'

# SQLite database (file banegi: students.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Table (Django model jaisa)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    course = db.Column(db.String(100))


@app.route('/', methods=['GET', 'POST'])  # GET = page open karna, POST = form submit karna
def home():

    if request.method == 'POST':  # agar user ne button dabaya hai → POST request aayi
        name = request.form.get('name') # HTML form se “name” field ka data le lo
        age = request.form.get('age')  # HTML form se “age” field ka data le lo
        course = request.form.get('course')  # HTML form se “course” field ka data le lo

        # # student ko list me add kar diya
        student = Student(name=name, age=age, course=course)
        db.session.add(student)
        db.session.commit()

        return redirect('/')  # Page reload krna
    
    students = Student.query.all()  # Student list me list karna
    return render_template("index.html", students=students)



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    student = Student.query.get(id)

    if request.method == 'POST':
        student.name = request.form.get('name')
        student.age = request.form.get('age')
        student.course = request.form.get('course')

        db.session.commit()
        return redirect('/')

    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/')




if __name__ == '__main__':
    with app.app_context():
         db.create_all()   # table auto create
    app.run(debug=True)