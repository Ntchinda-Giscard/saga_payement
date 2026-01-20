import httpx

class NotificationClient:
    def __init__(self, base_url: str = "http://localhost:8004"): # Notification Service
        self.base_url = base_url
    
    def send_notification(self, user_id: int, message: str, notification_type: str = "EMAIL"):
        payload = {
            "user_id": user_id,
            "message": message,
            "notification_type": notification_type
        }
        try:
            # Fire and forget or wait? Usually wait for 200 OK to confirm it's queued.
            httpx.post(f"{self.base_url}/notifications/send", json=payload, timeout=3.0)
        except Exception as e:
            print(f"Failed to send notification: {e}")
