from flask import Flask
from config import Config
from models import db
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()
print("POSTGRES:", os.getenv("DB_HOST"), os.getenv("DB_PORT"))

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app) 

with app.app_context():
    db.create_all()

from routes.students import students_bp
from routes.regions import regions_bp
from routes.geo import geo_bp
from routes.stats import stats_bp
from routes.reference import reference_bp
app.register_blueprint(reference_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(students_bp)
app.register_blueprint(regions_bp)
app.register_blueprint(geo_bp)

# === Запуск приложения ===
if __name__ == "__main__":
    app.run(debug=True)