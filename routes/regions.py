from flask import Blueprint, jsonify
from models import db, Region, District, Student

regions_bp = Blueprint("regions", __name__, url_prefix="/api")

@regions_bp.route("/regions", methods=["GET"])
def get_regions():
    regions = Region.query.all()
    result = []
    for region in regions:
        student_count = Student.query.filter_by(region_id=region.id).count()
        result.append({
            "id": region.id,
            "name": region.name,
            "latitude": region.latitude,
            "longitude": region.longitude,
            "students_count": student_count
        })
    return jsonify(result)

@regions_bp.route("/region/<int:region_id>/districts", methods=["GET"])
def get_districts_by_region(region_id):
    districts = District.query.filter_by(region_id=region_id).all()
    result = []
    for district in districts:
        student_count = Student.query.filter_by(district_id=district.id).count()
        result.append({
            "id": district.id,
            "name": district.name,
            "latitude": district.latitude,
            "longitude": district.longitude,
            "students_count": student_count
        })
    return jsonify(result)

@regions_bp.route("/district/<int:district_id>", methods=["GET"])
def get_students_by_district(district_id):
    students = Student.query.filter_by(district_id=district_id).all()
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
            "quota_id": s.quota_id,
            "gop_id": s.gop_id,
            "form_id": s.form_id
        })
    return jsonify(result)
