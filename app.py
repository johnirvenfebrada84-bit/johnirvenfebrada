from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Stallman"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Stallman"}
]

@app.route('/')
def home():
    return "Welcome to the Student API! Go to /students"

@app.route('/students')
def students_list():
    return jsonify(students)

@app.route('/add_student_form')
def form():
    html = """
    <h2>Add Student</h2>
    <form action="/add_student" method="POST">
    Name: <input type="text" name="name"><br><br>
    Grade: <input type="number" name="grade"><br><br>
    Section: <input type="text" name="section"><br><br>
    <button type="submit">Add</button>
    </form>
    """
    return render_template_string(html)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")

    new_student = {
        "id": len(students) + 1,
        "name": name,
        "grade": grade,
        "section": section
    }

    students.append(new_student)

    return jsonify({"message": "Student added", "student": new_student})

if __name__ == "__main__":
    app.run(debug=True)
