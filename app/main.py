from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.models import Pill, SessionLocal, init_db
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.cleanup import cleanup_old_entries

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# 0. List all pills
@app.get("/pills")
def list_all_pills(db: Session = Depends(get_db)):
    pills = db.query(Pill).all()
    for pill in pills:
        pill.fecha = pill.fecha.strftime("%d/%m/%Y")
    return pills

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

# 6. Edit pill by id
@app.put("/pills/{pill_id}")
def edit_pill(pill_id: int, color: str = None, dibujo: str = None, info: str = None, fecha: str = None, db: Session = Depends(get_db)):
    # Try to find the pill to edit
    pill = db.query(Pill).filter(Pill.id == pill_id).first()

    # If pill is not found, raise a 404 error
    if not pill:
        raise HTTPException(status_code=404, detail="No se encontró pastilla con ese ID.")
    
    # Update the pill's attributes if provided
    if color:
        pill.color = color
    if dibujo:
        pill.dibujo = dibujo
    if info:
        pill.info = info
    if fecha:
        try:
            # Accept dd/mm/yyyy format
            parsed_date = datetime.strptime(fecha, "%d/%m/%Y").date()
            pill.fecha = parsed_date
        except ValueError:
            raise HTTPException(status_code=400, detail="Fecha inválida.")
    
    # Commit changes to the database
    db.commit()
    db.refresh(pill)
    return {"message": "Pastilla actualizada con éxito.", "pill": pill.id}

# 5. Delete pill by id
@app.delete("/pills/{pill_id}")
def delete_pill(pill_id: int, db: Session = Depends(get_db)):
    # Try to find the pill to delete
    pill = db.query(Pill).filter(Pill.id == pill_id).first()

    # If pill is not found, raise a 404 error
    if not pill:
        raise HTTPException(status_code=404, detail="No se encontró pastilla con ese ID.")
    
    # If found, delete the pill
    db.delete(pill)
    db.commit()  # Commit changes to apply the deletion
    return {"message": "Pastilla eliminada con éxito."}

