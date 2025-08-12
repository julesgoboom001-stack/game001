import socket
import threading
import json

class GameClient:
    def __init__(self, on_message_received=None, host='localhost', port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.receive_thread = None
        self.on_message_received = on_message_received
        self.my_id = None

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()
            print(f"Connected to server at {self.host}:{self.port}")
            return True
        except ConnectionRefusedError:
            print("Connection refused. Is the server running?")
            return False

    def receive_messages(self):
        while True:
            try:
                message_bytes = self.client_socket.recv(1024)
                if not message_bytes:
                    break

                data = json.loads(message_bytes.decode('utf-8'))
                if data.get("type") == "welcome":
                    self.my_id = data["payload"]["id"]
                    print(f"My ID is {self.my_id}")
                elif self.on_message_received:
                    self.on_message_received(data)
                else:
                    print(f"Received from server: {data}")

            except json.JSONDecodeError:
                print("Received invalid JSON.")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        print("Disconnected from server.")
        self.client_socket.close()

    def send_message(self, message_type, payload):
        """Sends a message to the server."""
        self.send_data({"type": message_type, "payload": payload})

    def send_data(self, data):
        """Serializes data to JSON and sends it."""
        try:
            self.client_socket.send(json.dumps(data).encode('utf-8'))
        except:
            print("Failed to send data.")

    def close(self):
        self.client_socket.close()

if __name__ == '__main__':
    # Example usage
    def basic_message_handler(data):
        print(f"Received from server: {data}")

    client = GameClient(on_message_received=basic_message_handler)
    if client.connect():
        # Example of sending a message
        client.send_message("new_player", {"character_name": "TestClient"})

        # Keep the main thread alive to receive messages
        try:
            while True:
                msg = input("Enter message to send: ")
                client.send_message("chat_message", {"message": msg})
        except KeyboardInterrupt:
            client.close()
