import argparse
import os
import sys

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


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project_id", required=True, type=str, help="a Google Cloud Project ID")
    args = parser.parse_args()

    project_id = args.project_id
    creds = None
    sys.argv.clear()

    # look for existing Oauth token
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # create the token and save to file if missing or not valid/expired
    if not (creds or creds.valid()):
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            # creates local server for authentication and captures the response
            creds = flow.run_local_server()
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # build a gmail service object
    gmail_service = build("gmail", "v1", credentials=creds)
    # simple test to make sure the service is working
    print(dir(gmail_service))

    # simple test to make sure the service is working
    bq_service = build("bigquery", "v2", credentials=creds)
    query = {
        "query": """
        SELECT
          date,
          place_id
        FROM
          [bigquery-public-data:covid19_open_data.covid19_open_data]
        LIMIT 3
      """
    }

    response_json = bq_service.jobs().query(body=query, projectId=project_id).execute()
    rows = response_json.get("rows") or []
    for row in rows:
        print(rows)


if __name__ == "__main__":
    main(sys.argv[1:])
