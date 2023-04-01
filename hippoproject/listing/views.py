from django.shortcuts import render
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
import os.path

def index(request):

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'listing/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
    except HttpError as err:
        print(err)

    # Replace with your Google Sheet ID and range
    sheet_id = '170lKf3ocMNdO45OZTs9lbN-WQbS3u4jEWNlYMOP9_oI'
    sheet_range = 'Form Responses 1!A1:I31'

    # Call the Google Sheets API to fetch the data
    result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
    rows = result.get('values', [])

    # Pass the data to the render function as context
    context = {'data': rows}
    return render(request, 'index.html', context)