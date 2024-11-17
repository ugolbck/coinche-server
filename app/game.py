import random

from terminal_playing_cards import Deck, View
from app.models import Player, Team

class GameManager:
    def __init__(self):
        self.waiting_players: list[Player] = []
        self.active_games: dict[str, Game] = {}
        self.player_to_game_id: dict[Player, str] = {}
        self.game_id_counter = 0

    async def find_or_create_game(self, player: Player) -> str:
        self.waiting_players.append(player)

        if len(self.waiting_players) >= 4:
            game_id = f"game_{self.game_id_counter}"
            self.game_id_counter += 1
            players = self.waiting_players[:4]
            self.waiting_players = self.waiting_players[4:]

            # Assign players to a new game
            game = Game(game_id, players)
            self.active_games[game_id] = game
            
            # Notify players that the game has started
            for p in players:
                self.player_to_game_id[p] = game_id
                await p.websocket.send_text(f"game_id:{game_id} has started!")
            
            await game.init_game()
            
            return game_id
        return None
    
    async def broadcast_to_game(self, game_id: str, message: str):
        if game_id in self.active_games:
            for player in self.active_games[game_id].players:
                await player.websocket.send_text(message)
        else:
            raise ValueError(f"Game with id {game_id} not found")
    
    async def get_game_id_for_player(self, player: Player) -> str:
        if player in self.player_to_game_id:
            return self.player_to_game_id[player]
        return None

    async def remove_player(self, game_id: str, player: Player):
        if game_id in self.active_games:
            self.active_games[game_id].players.remove(player)
            if len(self.active_games[game_id].players) == 0:
                print(f"Game with id {game_id} has no players, deleting")
                del self.active_games[game_id]
        else:
            raise ValueError(f"Game with id {game_id} not found")


class Game:
    def __init__(self, game_id: str, players: list[Player]):
        self.game_id = game_id
        self.players = players
        self.state = "created"
        self.buffer = ""

        self.team_a: Team | None = None
        self.team_b: Team | None = None
        self._create_teams()

        self.round = 0

    
    async def init_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.deal_cards()
        self.state = "cards_dealt"
        self.turn = 0
        await self.send_cards_to_players()

    def deal_cards(self):
        # Deal three cards to each players
        for player in self.players:
            print(f"Dealing 3 cards to {player.name}")
            for _ in range(3):
                player.cards.append(self.deck.pop())

        # Deal two cards to each player
        for player in self.players:
            print(f"Dealing 2 cards to {player.name}")
            for _ in range(2):
                player.cards.append(self.deck.pop())

        # Deal three cards to each player
        for player in self.players:
            print(f"Dealing 3 cards to {player.name}")
            for _ in range(3):
                player.cards.append(self.deck.pop())

        # Assert that the deck is empty and each player has 8 cards
        assert all(len(player.cards) == 8 for player in self.players)
    
    def _create_teams(self):
        assert len(self.players) == 4
        random.shuffle(self.players)
        self.team_a = Team((self.players[0], self.players[1]))
        self.team_b = Team((self.players[2], self.players[3]))

    async def send_cards_to_players(self):
        for player in self.players:
            view = View(player.cards)
            print(f"Sending cards to {player.name}")
            print(type(view))
            print(view)
            await player.websocket.send_text(str(view))
