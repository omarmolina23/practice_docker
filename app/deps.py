from .database import SessionLocal
from sqlalchemy.orm import Session

# Dependency
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
