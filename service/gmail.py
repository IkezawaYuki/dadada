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


class Gmail:
    def __init__(self):
        self.creds = None
        self.subject = ""
        if os.path.exists('../token.json'):
            self.creds = Credentials.from_authorized_user_file("../token.json")
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "../credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            with open('../token.json', 'w') as token:
                token.write(self.creds.to_json())

    def set_title(self, subject):
        self.subject = subject

    def create_drafts(self, message_to, message_content):
        try:
            service = build("gmail", "v1", credentials=self.creds)
            message = EmailMessage()
            message.set_content(message_content)
            message["To"] = message_to
            message["From"] = "gduser2@workspacesamples.dev"
            message["Subject"] = self.subject
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"message": {"raw": encoded_message}}
            draft = (
                service.users()
                .drafts()
                .create(userId="me", body=create_message)
                .execute()
            )
            print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
        except HttpError as error:
            print(f"An error occurred: {error}")
            draft = None
        return draft
