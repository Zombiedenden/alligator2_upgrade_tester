## Tester to better understand how to use OAuth2 with Google APIs.

### My main objective is to test OAuth2 flows using:
- oauth2client
- google_auth_oauthlib

#### Installation steps:
- create GCP project
- Create Oauth consent screen
- Create OAuth 2.0 Client IDs credentials
- Download the credentials as json file client_secret.json
- Enable the Gmail API
- Enable the bigquery API (enabled by default)
- pip3 install requirements.txt

#### How to run
- python3 basic_tester.py --project_id=<PROJECT_ID>
- Note: make sure you replace the project_id with the one you created in the intstallation steps
