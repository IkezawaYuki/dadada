import os
import base64

from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]

content = """===================================

本メールは自動返信メールとなっております

===================================



この度はお問い合わせありがとうございます。


お問い合わせ内容を確認してご連絡を差し上げます。


引き続き宜しくお願い致します。"""


class Gmail:
    def __init__(self):
        self.creds = None
        print(os.path.exists('./token.json'))
        if os.path.exists('./token.json'):
            self.creds = Credentials.from_authorized_user_file("./token.json")
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "./credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            with open('./token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.service = build("gmail", "v1", credentials=self.creds)

    def follow_up_mail(self, message_to):
        try:
            message = EmailMessage()
            message.set_content(content)
            message["To"] = message_to
            message["From"] = "support@hp-standard.jp"
            message["Subject"] = "お問い合わせありがとうございます【ホームページスタンダード】"
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {"raw": encoded_message}
            send_message = (
                self.service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f'Message Id: {send_message["id"]}')
        except HttpError as error:
            print(f"An error occurred: {error}")
            send_message = None
        return send_message

    def create_drafts(self, message_to, message_content):
        try:
            message = EmailMessage()
            message.set_content(message_content)
            message["To"] = message_to
            message["From"] = "support@hp-standard.jp"
            message["Subject"] = "お問い合わせありがとうございます【ホームページスタンダード】"
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {"message": {"raw": encoded_message}}
            draft = (
                self.service.users()
                .drafts()
                .create(userId="me", body=create_message)
                .execute()
            )
            print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
        except HttpError as error:
            print(f"An error occurred: {error}")
            draft = None
        return draft
