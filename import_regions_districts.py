import pandas as pd
import requests
import time
from app import app
from models import db, Region, District

GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "student-map/1.0"}
FILE_PATH = "univer.xlsx"

def fetch_coordinates(query):
    params = {"q": query, "format": "json", "limit": 1}
    try:
        response = requests.get(GEOCODE_URL, params=params, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        print(f"[Ошибка геокодирования] {query}: {e}")
    return None, None

def import_regions_and_districts():
    df = pd.read_excel(FILE_PATH, sheet_name="univer")
    unique_pairs = df[["obl", "rai"]].dropna().drop_duplicates()

    with app.app_context():
        for _, row in unique_pairs.iterrows():
            region_name = row["obl"].strip()
            district_name = row["rai"].strip()

            # Создаём область, если нет
            region = Region.query.filter_by(name=region_name).first()
            if not region:
                lat, lon = fetch_coordinates(f"{region_name}, Казахстан")
                region = Region(name=region_name, latitude=lat, longitude=lon)
                db.session.add(region)
                db.session.commit()
                print(f"✅ Добавлена область: {region_name} ({lat}, {lon})")
                time.sleep(1)

            # Создаём район, если нет
            district = District.query.filter_by(name=district_name, region_id=region.id).first()
            if not district:
                query = f"{district_name}, {region_name}, Казахстан"
                lat, lon = fetch_coordinates(query)
                district = District(name=district_name, region_id=region.id,
                                    latitude=lat, longitude=lon)
                db.session.add(district)
                db.session.commit()
                print(f"✅ Добавлен район: {district_name} ({lat}, {lon})")
                time.sleep(1)

if __name__ == "__main__":
    import_regions_and_districts()
    print("🏁 Импорт регионов и районов завершён.")
