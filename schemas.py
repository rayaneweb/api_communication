from pydantic import BaseModel
from datetime import datetime


class CompteCreation(BaseModel):
    nom_utilisateur: str
    mot_de_passe: str


class CompteReponse(BaseModel):
    id: int
    nom_utilisateur: str

    model_config = {"from_attributes": True}


class LoginRequete(BaseModel):
    nom_utilisateur: str
    mot_de_passe: str


class TokenReponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageReponse(BaseModel):
    id: int
    expediteur_id: int
    destinataire_id: int
    contenu: str
    date_envoi: datetime

    model_config = {"from_attributes": True}
