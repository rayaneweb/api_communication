from fastapi import WebSocket


class GestionnaireConnexions:
    def __init__(self):
        self.actives: dict[int, WebSocket] = {}

    async def connecter(self, user_id: int, ws: WebSocket):
        await ws.accept()
        self.actives[user_id] = ws

    def deconnecter(self, user_id: int):
        self.actives.pop(user_id, None)

    async def envoyer(self, user_id: int, data: dict) -> bool:
        ws = self.actives.get(user_id)
        if ws is None:
            return False
        await ws.send_json(data)
        return True


gestionnaire = GestionnaireConnexions()
