import json
import requests


class Slack:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def request(self, payload):
        response = requests.post(
            self.webhook_url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )
        if response.status_code != 200:
            raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

    def send_alert(self, message):
        self.request({
            "icon_emoji": ":cold_sweat:",
            "username": "DADADA",
            "text": f"<@U04P797HYPM>\n{message}"
        })

    def send_message(self, message):
        self.request({
            "icon_emoji": ":wink:",
            "username": "DADADA",
            "text": message
        })
