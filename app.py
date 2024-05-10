import os
import logging

from flask import Flask, request, jsonify, render_template, redirect
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
def hello_world():
    hb_client = HubspotClient(hubspot_access_token)
    ticket_id = hb_client.create_ticket("Test [ikezawa_test]")
    print(ticket_id)
    # contact_id = hb_client.search_contact("yuki.ikezawa@strategy-drive.jp")
    # hb_client.associate(ticket_id, contact_id)
    return 'Hello World!'


@app.route("/dadada/flask-health-check")
def flask_health_check():
    return jsonify({"status": "ok"})


@app.get("/dadada/support/form")
def support_form_page():
    return render_template('index.html')


@app.get("/dadada/support/thank_you")
def support_thank_you_page():
    return render_template('thank_you.html')


@app.post("/dadada/support/form")
def support_form():
    # verification()
    form_data = request.form.to_dict()
    chatgpt = ChatGPT(aoai_api_key)
    aisearch = AiSearch(service_endpoint, index_name, key)
    hubspot = HubspotClient(hubspot_access_token)
    gmail = Gmail()
    gmail.follow_up_mail(form_data["email"])
    slack = Slack(slack_webhook_url)
    result = chatgpt.generate(form_data["content"])
    if result.choices[0].message.function_call:
        print("function call!!")
        slack.send_message("test test")
    else:
        body_message = result.choices[0].message.content
        gmail.create_drafts(form_data["email"], body_message)
        hubspot.create_ticket(form_data["content"])
    return redirect("/dadada/support/thank_you")


if __name__ == '__main__':
    app.run(port=8081)
