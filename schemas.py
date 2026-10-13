from pydantic import BaseModel


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
