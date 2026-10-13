from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models, schemas
from security import hasher_mot_de_passe
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from security import (
    hasher_mot_de_passe,
    verifier_mot_de_passe,
    creer_token,
    decoder_token,
)
from sqlalchemy import or_, and_

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


securite = HTTPBearer()


def utilisateur_courant(
    creds: HTTPAuthorizationCredentials = Depends(securite),
    db: Session = Depends(get_db),
):
    try:
        user_id = decoder_token(creds.credentials)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    utilisateur = db.get(models.Utilisateur, user_id)
    if not utilisateur:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable")
    return utilisateur


@app.post("/api/auth/login", response_model=schemas.TokenReponse)
def login(donnees: schemas.LoginRequete, db: Session = Depends(get_db)):
    utilisateur = (
        db.query(models.Utilisateur)
        .filter_by(nom_utilisateur=donnees.nom_utilisateur)
        .first()
    )
    if not utilisateur or not verifier_mot_de_passe(
        donnees.mot_de_passe, utilisateur.mot_de_passe_hash
    ):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    return {"access_token": creer_token(utilisateur.id), "token_type": "bearer"}


@app.get("/api/utilisateurs", response_model=list[schemas.CompteReponse])
def lister_utilisateurs(
    moi: models.Utilisateur = Depends(utilisateur_courant),
    db: Session = Depends(get_db),
):
    return db.query(models.Utilisateur).filter(models.Utilisateur.id != moi.id).all()


@app.get("/api/messages/{utilisateur_id}", response_model=list[schemas.MessageReponse])
def historique(
    utilisateur_id: int,
    moi: models.Utilisateur = Depends(utilisateur_courant),
    db: Session = Depends(get_db),
):
    if not db.get(models.Utilisateur, utilisateur_id):
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    return (
        db.query(models.Message)
        .filter(
            or_(
                and_(
                    models.Message.expediteur_id == moi.id,
                    models.Message.destinataire_id == utilisateur_id,
                ),
                and_(
                    models.Message.expediteur_id == utilisateur_id,
                    models.Message.destinataire_id == moi.id,
                ),
            )
        )
        .order_by(models.Message.date_envoi)
        .all()
    )
