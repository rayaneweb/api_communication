import bcrypt


def hasher_mot_de_passe(mdp: str) -> str:
    return bcrypt.hashpw(mdp.encode(), bcrypt.gensalt()).decode()


def verifier_mot_de_passe(mdp: str, hash_stocke: str) -> bool:
    return bcrypt.checkpw(mdp.encode(), hash_stocke.encode())
