import os
import logging

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import hmac
import hashlib

from service.chatgpt import ChatGPT
from service.gmail import Gmail
from service.hubspot_client import HubspotClient
from service.slack import Slack
from service.ai_search import AiSearch

load_dotenv()

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]
aoai_api_key = os.getenv("AOAI_API_KEY")
hubspot_access_token = os.getenv("HUBSPOT_ACCESS_TOKEN")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")


def verification():
    app.logger.debug('Verification started')
    received_data = request.get_data(as_text=True)
    received_signature = request.headers["Authorization"].replace("HMAC ", "")
    nonce = request.headers["X-Nonce"]
    timestamp = request.headers["X-Timestamp"]
    secret_key = os.getenv("API_SECRET")
    message = f"{received_data}{nonce}{timestamp}"
    signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
    if hmac.compare_digest(received_signature, signature) is False:
        return jsonify({"error": "Wrong signature"}), 401


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/dadada/flask-health-check")
def flask_health_check():
    return jsonify({"status": "ok"})


@app.post("/dadada/support/form")
def support_form():
    verification()
    received_data = request.get_json()
    chatgpt = ChatGPT(aoai_api_key)
    aisearch = AiSearch(service_endpoint, index_name, key)
    hubspot = HubspotClient(hubspot_access_token)
    gmail = Gmail()
    slack = Slack(slack_webhook_url)
    result = chatgpt.generate(received_data["content"])
    return jsonify("support/form!!!")


if __name__ == '__main__':
    app.run(port=8081)
