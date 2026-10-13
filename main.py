from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models, schemas
from security import hasher_mot_de_passe

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def accueil():
    return {"message": "Serveur de messagerie OK"}


@app.post("/api/comptes", response_model=schemas.CompteReponse, status_code=201)
def creer_compte(compte: schemas.CompteCreation, db: Session = Depends(get_db)):
    existant = (
        db.query(models.Utilisateur)
        .filter_by(nom_utilisateur=compte.nom_utilisateur)
        .first()
    )
    if existant:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")

    utilisateur = models.Utilisateur(
        nom_utilisateur=compte.nom_utilisateur,
        mot_de_passe_hash=hasher_mot_de_passe(compte.mot_de_passe),
    )
    db.add(utilisateur)
    db.commit()
    db.refresh(utilisateur)
    return utilisateur
