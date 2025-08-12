import socket
import threading
import json
import uuid

class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.clients = {}
        self.players = {}
        self.trade_sessions = {}
        self.teams = {}
        print(f"Server started on {host}:{port}")

    def listen(self):
        self.server_socket.listen(5)
        while True:
            client_socket, addr = self.server_socket.accept()
            player_id = str(uuid.uuid4())
            print(f"Accepted connection from {addr}, assigned player_id: {player_id}")
            self.clients[player_id] = client_socket

            # Send welcome message with the player's new ID
            client_socket.send(json.dumps({"type": "welcome", "payload": {"id": player_id}}).encode('utf-8'))

            thread = threading.Thread(target=self.handle_client, args=(client_socket, player_id))
            thread.start()

    def handle_client(self, client_socket, player_id):
        while True:
            try:
                message_bytes = client_socket.recv(1024)
                if not message_bytes:
                    self.remove_client(player_id)
                    break

                data = json.loads(message_bytes.decode('utf-8'))
                message_type = data.get("type")
                payload = data.get("payload")

                print(f"Received from {player_id}: {message_type} - {payload}")

                if message_type == "new_player":
                    self.players[player_id] = {
                        "id": player_id,
                        "character": payload["character_name"],
                        "x": 400,
                        "y": 300
                    }
                    # Notify all clients about the new player
                    self.broadcast("player_joined", self.players[player_id], player_id)
                    # Send existing players to the new client
                    client_socket.send(json.dumps({"type": "current_players", "payload": self.players}).encode('utf-8'))

                elif message_type == "player_moved":
                    if player_id in self.players:
                        self.players[player_id]["x"] = payload["x"]
                        self.players[player_id]["y"] = payload["y"]
                        self.broadcast("player_moved", self.players[player_id], player_id)

                elif message_type == "chat_message":
                    if player_id in self.players:
                        player_name = self.players[player_id]["character"]
                        message = f"{player_name}: {payload['message']}"
                        self.broadcast("new_chat_message", {"message": message})

                elif message_type == "trade_request":
                    target_id = payload["target_id"]
                    if target_id in self.clients:
                        self.clients[target_id].send(json.dumps({"type": "incoming_trade_request", "payload": {"from_id": player_id}}).encode('utf-8'))

                elif message_type == "trade_accepted":
                    requester_id = payload["requester_id"]
                    # Create a new trade session
                    trade_id = str(uuid.uuid4())
                    self.trade_sessions[trade_id] = {
                        "player1": requester_id,
                        "player2": player_id,
                        "player1_offer": [],
                        "player2_offer": [],
                        "player1_locked": False,
                        "player2_locked": False,
                        "player1_confirmed": False,
                        "player2_confirmed": False,
                    }
                    # Notify both players that the trade has started
                    self.clients[requester_id].send(json.dumps({"type": "trade_started", "payload": {"trade_id": trade_id, "other_player_id": player_id}}).encode('utf-8'))
                    self.clients[player_id].send(json.dumps({"type": "trade_started", "payload": {"trade_id": trade_id, "other_player_id": requester_id}}).encode('utf-8'))

                elif message_type == "trade_declined":
                    requester_id = payload["requester_id"]
                    if requester_id in self.clients:
                        self.clients[requester_id].send(json.dumps({"type": "trade_declined", "payload": {}}).encode('utf-8'))

                elif message_type == "trade_offer_update":
                    trade_id = payload["trade_id"]
                    if trade_id in self.trade_sessions:
                        session = self.trade_sessions[trade_id]
                        other_player = session["player2"] if session["player1"] == player_id else session["player1"]
                        if session["player1"] == player_id:
                            session["player1_offer"] = payload["offer"]
                        else:
                            session["player2_offer"] = payload["offer"]

                        self.clients[other_player].send(json.dumps({"type": "trade_offer_update", "payload": {"offer": payload["offer"]}}).encode('utf-8'))

                elif message_type == "trade_cancel":
                    trade_id = payload["trade_id"]
                    if trade_id in self.trade_sessions:
                        session = self.trade_sessions[trade_id]
                        # Notify both players
                        self.clients[session["player1"]].send(json.dumps({"type": "trade_canceled"}).encode('utf-8'))
                        self.clients[session["player2"]].send(json.dumps({"type": "trade_canceled"}).encode('utf-8'))
                        del self.trade_sessions[trade_id]

                elif message_type == "trade_confirm":
                    trade_id = payload["trade_id"]
                    if trade_id in self.trade_sessions:
                        session = self.trade_sessions[trade_id]
                        if session["player1"] == player_id:
                            session["player1_confirmed"] = True
                        else:
                            session["player2_confirmed"] = True

                        if session["player1_confirmed"] and session["player2_confirmed"]:
                            # Both players confirmed, finalize the trade
                            player1_id = session["player1"]
                            player2_id = session["player2"]

                            # Send offers to the other player
                            self.clients[player1_id].send(json.dumps({"type": "trade_finalized", "payload": {"received_items": session["player2_offer"]}}).encode('utf-8'))
                            self.clients[player2_id].send(json.dumps({"type": "trade_finalized", "payload": {"received_items": session["player1_offer"]}}).encode('utf-8'))

                            del self.trade_sessions[trade_id]

                elif message_type == "team_invite":
                    target_id = payload["target_id"]
                    if target_id in self.clients:
                        self.clients[target_id].send(json.dumps({"type": "incoming_team_invite", "payload": {"from_id": player_id}}).encode('utf-8'))

                elif message_type == "team_invite_accepted":
                    requester_id = payload["requester_id"]
                    # Find if the requester is already in a team
                    requester_team = None
                    for team_id, team in self.teams.items():
                        if requester_id in team["members"]:
                            requester_team = team_id
                            break

                    if requester_team:
                        self.teams[requester_team]["members"].append(player_id)
                        team_members = self.teams[requester_team]["members"]
                    else:
                        team_id = str(uuid.uuid4())
                        self.teams[team_id] = {"members": [requester_id, player_id]}
                        team_members = self.teams[team_id]["members"]

                    # Notify all team members of the update
                    for member_id in team_members:
                        if member_id in self.clients:
                            self.clients[member_id].send(json.dumps({"type": "team_update", "payload": {"members": team_members}}).encode('utf-8'))

                elif message_type == "team_invite_declined":
                    requester_id = payload["requester_id"]
                    if requester_id in self.clients:
                        self.clients[requester_id].send(json.dumps({"type": "team_invite_declined", "payload": {}}).encode('utf-8'))

            except json.JSONDecodeError:
                print(f"Received invalid JSON from {player_id}")
            except Exception as e:
                print(f"Error handling client {player_id}: {e}")
                self.remove_client(player_id)
                break

    def broadcast(self, message_type, payload, sender_id=None):
        message = json.dumps({"type": message_type, "payload": payload})

        # For chat messages, we want to send to everyone, including the sender.
        if message_type == "new_chat_message":
            for player_id, client_socket in self.clients.items():
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    self.remove_client(player_id)
        else: # For other messages, we exclude the sender
            for player_id, client_socket in self.clients.items():
                if player_id != sender_id:
                    try:
                        client_socket.send(message.encode('utf-8'))
                    except:
                        self.remove_client(player_id)

    def remove_client(self, player_id):
        if player_id in self.clients:
            del self.clients[player_id]
        if player_id in self.players:
            del self.players[player_id]
            self.broadcast("player_left", {"id": player_id})
        print(f"Client {player_id} disconnected.")

if __name__ == "__main__":
    server = GameServer()
    server.listen()
