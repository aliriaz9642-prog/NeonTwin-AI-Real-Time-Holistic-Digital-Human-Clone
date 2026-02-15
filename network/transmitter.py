import socket
import json

class PoseTransmitter:
    def __init__(self, ip="127.0.0.1", port=5005):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_payload(self, payload):
        """
        Sends a structured dictionary payload to Unity.
        """
        if payload is None:
            return

        message = json.dumps(payload).encode('utf-8')
        
        try:
            # Check size to prevent MTU issues (highly unlikely for pose data)
            self.sock.sendto(message, (self.ip, self.port))
        except Exception as e:
            print(f"Network Error: {e}")

    def close(self):
        self.sock.close()
