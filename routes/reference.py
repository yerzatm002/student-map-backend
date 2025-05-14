from flask import Blueprint, jsonify
from models import Form, Quota, GOP

reference_bp = Blueprint("reference", __name__, url_prefix="/api")

@reference_bp.route("/forms", methods=["GET"])
def get_forms():
    forms = Form.query.all()
    return jsonify([{"id": f.id, "name": f.name} for f in forms])

@reference_bp.route("/quotas", methods=["GET"])
def get_quotas():
    quotas = Quota.query.all()
    return jsonify([{"id": q.id, "name": q.name} for q in quotas])

@reference_bp.route("/gops", methods=["GET"])
def get_gops():
    gops = GOP.query.all()
    return jsonify([{"id": g.id, "name": g.name} for g in gops])
