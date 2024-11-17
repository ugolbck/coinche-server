from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.game import GameManager
from app.models import Player


app = FastAPI(title="Coinche server", version="0.1.0")


# CORS to allow the client to access the API from another origin (other domain, other port, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Root"], summary="Health endpoint")
def health():
    return {"message": "Healthy!"}


game_manager = GameManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Initialize player
    player = Player(websocket=websocket, name=f"{websocket.client.host}:{websocket.client.port}")

    try:
        # Find or create a game for the player
        game_id = await game_manager.find_or_create_game(player)
        if game_id:
            print(f"Player {websocket.client.host}:{websocket.client.port} connected to game {game_id}")
        else:
            print(f"Player {websocket.client.host}:{websocket.client.port} connected to lobby")

        while True:
            # Receive data from the player
            data = await websocket.receive_text()
            print(f"Received data from {websocket.client.host}:{websocket.client.port} -> {data}")
            
            game_id = await game_manager.get_game_id_for_player(player)
            if game_id:
                # Broadcast data to all players in the game
                await game_manager.broadcast_to_game(game_id, data)
    except WebSocketDisconnect:
        if game_id:
            await game_manager.remove_player(game_id, player)
