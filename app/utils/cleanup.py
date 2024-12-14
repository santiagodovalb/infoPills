from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from database.models import Pill, SessionLocal

def cleanup_old_entries():
    db = SessionLocal()
    try:
        one_year_ago = datetime.now().date() - timedelta(days=365)
        old_entries = db.query(Pill).filter(Pill.fecha < one_year_ago).all()
        if old_entries:
            for pill in old_entries:
                db.delete(pill)
            db.commit()
            print(f"Deleted {len(old_entries)} old entries.")
    except Exception as e:
        print("Error during cleanup:", e)
    finally:
        db.close()
