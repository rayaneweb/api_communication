from pydantic import BaseModel


class CompteCreation(BaseModel):
    nom_utilisateur: str
    mot_de_passe: str


class CompteReponse(BaseModel):
    id: int
    nom_utilisateur: str

    model_config = {"from_attributes": True}
