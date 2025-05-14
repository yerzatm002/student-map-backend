import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from config import Config
from models import db

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
CORS(app)

# === Регистрация маршрутов ===
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

# === Запуск приложения (Render ищет PORT) ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_ENV") != "production")
