from flask import Flask, request, render_template_string, redirect, url_for, jsonify

app = Flask(__name__)

students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Stallman"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Stallman"}
]

# DASHBOARD
@app.route('/')
def home():

    search = request.args.get("search")
    filtered_students = students

    if search:
        filtered_students = [s for s in students if search.lower() in s["name"].lower()]

    rows = ""

    for s in filtered_students:
        rows += f"""
        <tr>
        <td>{s['id']}</td>
        <td>{s['name']}</td>
        <td>{s['grade']}</td>
        <td>{s['section']}</td>
        <td>
        <a href="/edit/{s['id']}">Edit</a>
        <a href="/delete/{s['id']}">Delete</a>
        </td>
        </tr>
        """

    html = f"""
    <html>
    <head>
    <title>Student Management System</title>

    <style>

    body {{
        font-family: Arial;
        background:#e8f5e9;
        text-align:center;
    }}

    h1 {{
        background:#2e7d32;
        color:white;
        padding:20px;
    }}

    table {{
        width:80%;
        margin:20px auto;
        border-collapse:collapse;
        background:white;
    }}

    th,td {{
        padding:12px;
        border:1px solid #ddd;
    }}

    th {{
        background:#43a047;
        color:white;
    }}

    a {{
        text-decoration:none;
        padding:6px 12px;
        color:white;
        border-radius:4px;
    }}

    a[href*="edit"] {{
        background:#388e3c;
    }}

    a[href*="delete"] {{
        background:#c62828;
    }}

    .add {{
        background:#43a047;
        padding:10px 20px;
        margin:10px;
        display:inline-block;
    }}

    input {{
        padding:8px;
        width:200px;
    }}

    button {{
        padding:8px 12px;
        background:#2e7d32;
        color:white;
        border:none;
        border-radius:4px;
        cursor:pointer;
    }}

    button:hover {{
        background:#1b5e20;
    }}

    </style>
    </head>

    <body>

    <h1>Student Management System</h1>

    <form method="GET">
    <input type="text" name="search" placeholder="Search student">
    <button type="submit">Search</button>
    </form>

    <br>

    <a class="add" href="/add">Add Student</a>

    <table>

    <tr>
    <th>ID</th>
    <th>Name</th>
    <th>Grade</th>
    <th>Section</th>
    <th>Action</th>
    </tr>

    {rows}

    </table>

    <br>

    <h3>Analytics</h3>

    <a class="add" href="/average">Average Grade</a>
    <a class="add" href="/pass_fail">Pass / Fail Count</a>
    <a class="add" href="/performance">Performance Summary</a>

    </body>
    </html>
    """

    return render_template_string(html)


# ADD STUDENT
@app.route('/add', methods=['GET','POST'])
def add():

    if request.method == "POST":

        name = request.form["name"]
        grade = request.form["grade"]
        section = request.form["section"]

        new_student = {
            "id": len(students) + 1,
            "name": name,
            "grade": int(grade),
            "section": section
        }

        students.append(new_student)

        return redirect(url_for("home"))

    html = """
    <h2>Add Student</h2>

    <form method="POST">

    Name:<br>
    <input type="text" name="name"><br><br>

    Grade:<br>
    <input type="number" name="grade"><br><br>

    Section:<br>
    <input type="text" name="section"><br><br>

    <button type="submit">Add Student</button>

    </form>

    <br>
    <a href="/">Back</a>
    """

    return render_template_string(html)


# EDIT STUDENT
@app.route('/edit/<int:id>')
def edit(id):

    student = None

    for s in students:
        if s["id"] == id:
            student = s

    html = f"""
    <h2>Edit Student</h2>

    <form action="/update/{id}" method="POST">

    Name:<br>
    <input type="text" name="name" value="{student['name']}"><br><br>

    Grade:<br>
    <input type="number" name="grade" value="{student['grade']}"><br><br>

    Section:<br>
    <input type="text" name="section" value="{student['section']}"><br><br>

    <button type="submit">Update Student</button>

    </form>

    <br>
    <a href="/">Back</a>
    """

    return render_template_string(html)


# UPDATE STUDENT
@app.route('/update/<int:id>', methods=['POST'])
def update(id):

    for s in students:
        if s["id"] == id:
            s["name"] = request.form["name"]
            s["grade"] = int(request.form["grade"])
            s["section"] = request.form["section"]

    return redirect(url_for("home"))


# DELETE STUDENT
@app.route('/delete/<int:id>')
def delete(id):

    global students
    students = [s for s in students if s["id"] != id]

    return redirect(url_for("home"))


# AVERAGE GRADE
@app.route('/average')
def average():

    total = sum(s["grade"] for s in students)
    count = len(students)

    avg = total / count if count > 0 else 0

    return jsonify({
        "average_grade": round(avg,2),
        "total_students": count
    })


# PASS FAIL COUNT
@app.route('/pass_fail')
def pass_fail():

    passed = len([s for s in students if s["grade"] >= 75])
    failed = len([s for s in students if s["grade"] < 75])

    return jsonify({
        "passed_students": passed,
        "failed_students": failed
    })


# PERFORMANCE SUMMARY
@app.route('/performance')
def performance():

    total = len(students)

    avg = sum(s["grade"] for s in students) / total if total > 0 else 0

    passed = len([s for s in students if s["grade"] >= 75])
    failed = len([s for s in students if s["grade"] < 75])

    # Convert grade to text
    grade_summary = [{"name": s["name"], "grade": s["grade"], "result": "Pass" if s["grade"]>=75 else "Fail"} for s in students]

    return jsonify({
        "total_students": total,
        "average_grade": round(avg,2),
        "passed_students": passed,
        "failed_students": failed,
        "grades": grade_summary
    })


if __name__ == "__main__":
    app.run(debug=True)
