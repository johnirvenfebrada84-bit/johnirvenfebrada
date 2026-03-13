from flask import Flask, jsonify, request, render_template, redirect, url_for
import uuid

app = Flask(__name__)

# --- Data Storage ---
students = []
grades = []

# --- Helper Functions ---
def get_student_grades(student_id):
    return [g for g in grades if g["student_id"] == student_id]

def calculate_average(student_id):
    student_grades = get_student_grades(student_id)
    if not student_grades:
        return 0
    return round(sum(g["score"] for g in student_grades) / len(student_grades), 2)

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html',
                           students=students,
                           grades=grades,
                           get_student_grades=get_student_grades,
                           calculate_average=calculate_average)

# --- API Routes ---

# Add Student
@app.route('/api/student/add', methods=['POST'])
def api_add_student():
    data = request.json
    if not data or not all(k in data for k in ['name', 'age', 'section']):
        return jsonify({"error": "Missing data"}), 400

    new_student = {
        "id": str(uuid.uuid4()),
        "name": data['name'],
        "age": int(data['age']),
        "section": data['section']
    }
    students.append(new_student)
    return jsonify({"success": True, "student": new_student})

# Edit Student
@app.route('/api/student/edit/<student_id>', methods=['POST'])
def api_edit_student(student_id):
    data = request.json
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    student["name"] = data.get("name", student["name"])
    student["age"] = int(data.get("age", student["age"]))
    student["section"] = data.get("section", student["section"])
    return jsonify({"success": True, "student": student})

# Delete Student
@app.route('/api/student/delete/<student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    global students, grades
    students = [s for s in students if s["id"] != student_id]
    grades = [g for g in grades if g["student_id"] != student_id]
    return jsonify({"success": True})

# Add Grade
@app.route('/api/grade/add', methods=['POST'])
def api_add_grade():
    data = request.json
    new_grade = {
        "id": str(uuid.uuid4()),
        "student_id": data["student_id"],
        "subject": data["subject"],
        "score": int(data["score"])
    }
    grades.append(new_grade)
    return jsonify({"success": True, "grade": new_grade})

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)
