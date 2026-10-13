import bcrypt
import jwt
from datetime import datetime, timedelta, timezone


def hasher_mot_de_passe(mdp: str) -> str:
    return bcrypt.hashpw(mdp.encode(), bcrypt.gensalt()).decode()


def verifier_mot_de_passe(mdp: str, hash_stocke: str) -> bool:
    return bcrypt.checkpw(mdp.encode(), hash_stocke.encode())


SECRET_KEY = "change-moi-plus-tard"
ALGORITHM = "HS256"
DUREE_TOKEN_MIN = 60


def creer_token(utilisateur_id: int) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=DUREE_TOKEN_MIN)
    return jwt.encode(
        {"sub": str(utilisateur_id), "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM
    )


def decoder_token(token: str) -> int:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return int(payload["sub"])
