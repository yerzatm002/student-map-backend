import pandas as pd
from models import db, Region, District, GOP, Student
from app import app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FILE_PATH = "univer.xlsx"

def import_students_from_univer(xls):
    df = xls.parse("univer")
    logger.info(f"Найдено записей: {len(df)}")

    for index, row in df.iterrows():
        try:
            full_name = row.get("FIO")
            group = row.get("grup")
            course = row.get("kurs")
            gop_name = row.get("spec")
            lang = row.get("lang")
            region_name = row.get("obl")
            district_name = row.get("rai")

            if not full_name:
                logger.warning(f"[{index}] Пропущено: нет ФИО")
                continue

            region = Region.query.filter_by(name=region_name).first()
            if not region:
                logger.warning(f"[{index}] Не найдена область: {region_name}")
                continue

            district = District.query.filter_by(name=district_name, region_id=region.id).first()
            if not district:
                logger.warning(f"[{index}] Не найден район: {district_name}")
                continue

            gop = GOP.query.filter_by(name=gop_name).first()
            if not gop:
                gop = GOP(name=gop_name)
                db.session.add(gop)
                db.session.commit()
                logger.info(f"[{index}] Добавлен новый GOP: {gop_name}")

            student = Student(
                full_name=full_name,
                group=group,
                course=int(course) if pd.notnull(course) else None,
                lang=lang,
                region_id=region.id,
                district_id=district.id,
                gop_id=gop.id
            )

            db.session.add(student)
            db.session.commit()
            logger.info(f"[{index}] Добавлен студент: {full_name}")

        except Exception as e:
            db.session.rollback()
            logger.error(f"[{index}] Ошибка при добавлении: {full_name} — {e}")

if __name__ == "__main__":
    with app.app_context():
        xls = pd.ExcelFile(FILE_PATH)
        import_students_from_univer(xls)
        logger.info("Импорт из univer.xlsx завершён.")
