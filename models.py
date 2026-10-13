from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base


class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom_utilisateur = Column(String(50), unique=True, nullable=False)
    mot_de_passe_hash = Column(String(255), nullable=False)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    expediteur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    destinataire_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    contenu = Column(Text, nullable=False)
    date_envoi = Column(DateTime, default=datetime.utcnow)
