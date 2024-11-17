from terminal_playing_cards import Card
from fastapi import WebSocket


class Player:
    def __init__(self, websocket: WebSocket, name: str):
        self.websocket = websocket
        self.name = name
        self.cards: list[Card] = []

    def __hash__(self):
        # Use the websocket's hash as the player's hash
        return hash(self.websocket)
    
    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self.websocket == other.websocket


class Team:
    def __init__(self, players: tuple[Player, Player]):
        assert len(players) == 2
        self.players = players
        self.score = 0