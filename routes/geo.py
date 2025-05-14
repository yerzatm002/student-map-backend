from flask import Blueprint, jsonify
from models import Region, District

geo_bp = Blueprint("geo", __name__, url_prefix="/api/geo")

@geo_bp.route("/regions", methods=["GET"])
def geo_regions():
    features = []
    for region in Region.query.all():
        if not region.latitude or not region.longitude:
            continue
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [region.longitude, region.latitude]
            },
            "properties": {
                "id": region.id,
                "name": region.name
            }
        })
    return jsonify({
        "type": "FeatureCollection",
        "features": features
    })

@geo_bp.route("/region/<int:region_id>", methods=["GET"])
def geo_region_districts(region_id):
    features = []
    for district in District.query.filter_by(region_id=region_id).all():
        if not district.latitude or not district.longitude:
            continue
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [district.longitude, district.latitude]
            },
            "properties": {
                "id": district.id,
                "name": district.name
            }
        })
    return jsonify({
        "type": "FeatureCollection",
        "features": features
    })
