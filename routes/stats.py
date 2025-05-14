from flask import Blueprint, jsonify
from models import db, Student, Quota, Form, GOP, Region
from sqlalchemy import func

stats_bp = Blueprint("stats", __name__, url_prefix="/api/stats")

@stats_bp.route("", methods=["GET"])
def get_stats():
    stats = {
        "total_students": Student.query.count(),
        "by_gop": [],
        "by_course": [],
        "by_region": []
    }


    # ГОП
    gops = db.session.query(GOP.name, func.count(Student.id))\
        .join(Student, Student.gop_id == GOP.id)\
        .group_by(GOP.name).all()
    for name, count in gops:
        stats["by_gop"].append({"gop": name, "count": count})

    # Курсы
    courses = db.session.query(Student.course, func.count(Student.id))\
        .group_by(Student.course).all()
    for course, count in courses:
        stats["by_course"].append({"course": course, "count": count})

    # Регионы
    regions = db.session.query(Region.name, func.count(Student.id))\
        .join(Region, Region.id == Student.region_id)\
        .group_by(Region.name).all()
    for name, count in regions:
        stats["by_region"].append({"region": name, "count": count})

    return jsonify(stats)
