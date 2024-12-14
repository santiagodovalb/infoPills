from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import Pill, SessionLocal, init_db
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

scheduler = BackgroundScheduler()

# Initialize the database on startup
@app.on_event("startup")
def startup():
    init_db()
    scheduler.add_job(cleanup_old_entries, 'interval', days=1)
    scheduler.start()

@app.on_event("shutdown")
def shutdown():
    scheduler.shutdown()

# Dependency for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. List all pill colors
@app.get("/pills/colores")
def list_pill_colors(db: Session = Depends(get_db)):
    colors = db.query(Pill.color).distinct().all()
    return [color[0] for color in colors]  # Extract colors from tuples

# 2. List all pill names by color
@app.get("/pills/dibujos")
def list_pill_names_by_color(color: str, db: Session = Depends(get_db)):
    names = db.query(Pill.dibujo).filter(Pill.color == color).all()
    if not names:
        raise HTTPException(status_code=404, detail="No hay pastillas de ese color.")
    return [name[0] for name in names]  # Extract names from tuples

# 3. Get pill info by color and name
@app.get("/pills/info")
def get_pill_info(color: str, dibujo: str, db: Session = Depends(get_db)):
    pill = db.query(Pill).filter(Pill.color == color, Pill.dibujo == dibujo).first()
    if not pill:
        raise HTTPException(status_code=404, detail="No se encontró pastilla de ese color y dibujo.")
    formatted_date = pill.fecha.strftime("%d/%m/%Y")
    return {"info": pill.info, "date": formatted_date}

# 4. Add a new pill to the database
@app.post("/pills")
def add_pill(color: str, dibujo: str, info: str, fecha: str, db: Session = Depends(get_db)):
    try:
        # Accept dd/mm/yyyy format
        parsed_date = datetime.strptime(fecha, "%d/%m/%Y").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Fecha inválida.")

    # Create and add a new pill
    new_pill = Pill(color=color, dibujo=dibujo, info=info, fecha=parsed_date)
    db.add(new_pill)
    db.commit()
    db.refresh(new_pill)
    return {"message": "Pastilla añadida con éxito.", "pill": new_pill.id}