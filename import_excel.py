import pandas as pd
from models import db, Region, District, Form, Quota, GOP, Student
from app import app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


FILE_PATH = "Прием_ком_1.xlsx"

def import_regions(xls):
    df = xls.parse("обл")
    for _, row in df[1:].iterrows():
        name = row.iloc[1]
        if not name or Region.query.filter_by(name=name).first():
            continue
        region = Region(name=name)
        db.session.add(region)
        logger.info(f"Добавлена область: {name}")
    db.session.commit()

def import_districts(xls):
    df = xls.parse("обл_рай")
    for _, row in df[1:].iterrows():
        region_name = row.iloc[1]
        district_name = row.iloc[2]
        region = Region.query.filter_by(name=region_name).first()
        if not region or not district_name or \
           District.query.filter_by(name=district_name, region=region).first():
            continue
        district = District(name=district_name, region=region)
        db.session.add(district)
        logger.info(f"Добавлен район: {district_name} (область: {region_name})")
    db.session.commit()

def import_forms(xls):
    df = xls.parse("форм_обуч")
    for _, row in df[1:].iterrows():
        name = row.iloc[1]
        if not name or Form.query.filter_by(name=name).first():
            continue
        db.session.add(Form(name=name))
        logger.info(f"Добавлена форма обучения: {name}")
    db.session.commit()

def import_quotas(xls):
    df = xls.parse("квота")
    for _, row in df[1:].iterrows():
        name = row.iloc[1]
        if not name or Quota.query.filter_by(name=name).first():
            continue
        db.session.add(Quota(name=name))
        logger.info(f"Добавлена квота: {name}")
    db.session.commit()

def import_gops(xls):
    df = xls.parse("ГОП")
    for _, row in df[1:].iterrows():
        name = row.iloc[1]
        if not name or GOP.query.filter_by(name=name).first():
            continue
        db.session.add(GOP(name=name))
        logger.info(f"Добавлен ГОП: {name}")
    db.session.commit()

def import_students(xls):
    df = xls.parse("file", header=5)
    df.columns = df.columns.str.strip()
    logger.info(f"Колонки Excel: {df.columns.tolist()}")

    for index, row in df.iterrows():
        try:
            fio = row.get("ФИО")
            iin_raw = row.get("ИИН")
            iin = str(iin_raw).strip() if pd.notnull(iin_raw) else None

            if not fio or not iin:
                logger.warning(f"[{index}] Пропущено: отсутствует ФИО или ИИН")
                continue

            if Student.query.filter_by(iin=iin).first():
                logger.warning(f"[{index}] Пропущено: дубликат ИИН {iin}")
                continue

            region = Region.query.filter_by(name=row.get("Область")).first()
            if not region:
                logger.warning(f"[{index}] Пропущено: не найдена область {row.get('Область')}")
                continue

            district = None
            if row.get("Район"):
                district = District.query.filter_by(name=row.get("Район"), region=region).first()

            form = Form.query.filter_by(name=row.get("Форма обучения")).first()
            quota = Quota.query.filter_by(name=row.get("Квота")).first()
            gop = GOP.query.filter_by(name=row.get("ГОП")).first()

            student = Student(
                fio=fio,
                phone=row.get("Телефон школы"),
                iin=iin,
                school=row.get("Школа"),
                score=row.get("Сумма Конкурсного балла", 0),
                region_id=region.id if region else None,
                district_id=district.id if district else None,
                form_id=form.id if form else None,
                quota_id=quota.id if quota else None,
                gop_id=gop.id if gop else None,
            )

            db.session.add(student)
            db.session.commit()  
            logger.info(f"[{index}] Добавлен студент: {fio}, ИИН: {iin}")

        except Exception as e:
            db.session.rollback()  
            logger.error(f"[{index}] Ошибка при добавлении студента: {fio}, ИИН: {iin} — {e}")

if __name__ == "__main__":
    with app.app_context():
        xls = pd.ExcelFile(FILE_PATH)
        import_regions(xls)
        import_districts(xls)
        import_forms(xls)
        import_quotas(xls)
        import_gops(xls)
        import_students(xls)
        logger.info("Импорт завершён успешно.")
