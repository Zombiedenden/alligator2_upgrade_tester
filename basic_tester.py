import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CLIENT_SECRET_FILE = "client_secret.json"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/bigquery",
    # 'https://mail.google.com/'
]


def main():
    creds = None
    # look for existing Oauth token
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # create the token and save to file if missing or not valid/expired
    if not (creds or creds.valid()):
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            # creates local server for authentication and captures the response
            creds = flow.run_local_server()
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # build a gmail service object
    service_gmail = build("gmail", "v1", credentials=creds)
    # simple test to make sure the service is working
    print(dir(service_gmail))


if __name__ == "__main__":
    main()
