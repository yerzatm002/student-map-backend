from flask import Blueprint, request, jsonify
from models import db, Student

students_bp = Blueprint("students", __name__, url_prefix="/api/students")

@students_bp.route("", methods=["GET"])
def get_students():
    students = Student.query.all()
    result = []
    for s in students:
        result.append({
            "id": s.id,
            "full_name": s.full_name,
            "group": s.group,
            "course": s.course,
            "lang": s.lang,
            "iin": s.iin,
            "school": s.school,
            "score": s.score,
            "region_id": s.region_id,
            "district_id": s.district_id,
            "quota_id": s.quota_id,
            "gop_id": s.gop_id,
            "form_id": s.form_id,
        })
    return jsonify(result)

@students_bp.route("", methods=["POST"])
def add_student():
    data = request.get_json()
    try:
        student = Student(
            full_name=data.get("full_name"),
            group=data.get("group"),
            course=data.get("course"),
            lang=data.get("lang"),
            iin=str(data.get("iin")),
            school=data.get("school"),
            score=data.get("score"),
            region_id=data.get("region_id"),
            district_id=data.get("district_id"),
            quota_id=data.get("quota_id"),
            gop_id=data.get("gop_id"),
            form_id=data.get("form_id")
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({"message": "Студент добавлен"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@students_bp.route("/upload", methods=["POST"])
def upload_excel():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Файл не передан"}), 400
    try:
        from import_univer import import_students_from_univer
        import pandas as pd
        xls = pd.ExcelFile(file)
        import_students_from_univer(xls)
        return jsonify({"message": "Импорт завершён"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
