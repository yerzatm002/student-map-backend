import requests
from app import app
from models import db, Region, District
import time

GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "student-map/1.0"}


def fetch_coordinates(query):
    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }
    try:
        response = requests.get(GEOCODE_URL, params=params, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        print(f"Ошибка при получении координат для {query}: {e}")
    return None, None


def update_region_coordinates():
    with app.app_context():
        regions = Region.query.all()
        for region in regions:
            if region.latitude and region.longitude:
                continue
            query = f"{region.name}, Казахстан"
            lat, lon = fetch_coordinates(query)
            if lat and lon:
                region.latitude = lat
                region.longitude = lon
                db.session.commit()
                print(f"{region.name} — lat: {lat}, lon: {lon}")
            else:
                print(f"Не удалось найти координаты для {region.name}")
            time.sleep(1)  # Уважение к API


def update_district_coordinates():
    with app.app_context():
        districts = District.query.all()
        for district in districts:
            if district.latitude and district.longitude:
                continue
            region = Region.query.get(district.region_id)
            query = f"{district.name}, {region.name}, Казахстан"
            lat, lon = fetch_coordinates(query)
            if lat and lon:
                district.latitude = lat
                district.longitude = lon
                db.session.commit()
                print(f"{district.name} — lat: {lat}, lon: {lon}")
            else:
                print(f"Не удалось найти координаты для {district.name}")
            time.sleep(1)


if __name__ == "__main__":
    update_region_coordinates()
    update_district_coordinates()
    print("Геокодинг завершён")
